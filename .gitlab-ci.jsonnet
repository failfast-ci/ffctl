local utils = import ".gitlab-ci/utils.libsonnet";
local baseJob = utils.baseJob;
local mergeJob = utils.ci.mergeJob;

local stages_list = [
  // gitlab-ci stages
  "docker_build",
  "unit_tests",
  "integration",
];

local stages = utils.set(stages_list);

local vars = {
  global: {
    // .gitlab-ci.yaml top `variables` key
    FAILFASTCI_NAMESPACE: "quay",
  },

  // internal variables
  image: {
    repo: "quay.io/quay/quay-ci",
    tag: "${CI_COMMIT_REF_SLUG}",
    name: utils.containerName(self.repo, self.tag),
  },

  baseimage: {
    repo: "quay.io/quay/quay-ci",
    tag: "latest",
    name: utils.containerName(self.repo, self.tag),
  },
};


local container_builds = mergeJob(baseJob.dockerBuild, {
  "container-base-build": {
    // Always re-run the base build container on master merge
    // Docker tag is 'latest'.
    script: [
      "docker build --cache-from quay.io/quay/quay-base:latest" +
      " -t %s -f quay-base.dockerfile ." % vars.baseimage.name,
      "docker push %s" % vars.baseimage.name,
    ],
    only: ['master', 'tags'] },

  "container-base-build-branch": self['container-base-build'] {
    // Run the base build on-demand on branches
    only: ['branches'],
    when: 'manual',
  },

  "container-build-branch": {
    // Build and push the quay container.
    // Docker Tag is the branch/tag name
    script: [
      "docker build -t %s -f quay.dockerfile ." % vars.image.name,
      "docker push %s" % vars.image.name],
    only: ['master, tags'] },

  "container-build": self['container-build-branch'] {
    // On master branch also tag the container with the commit sha
    local repo_with_sha = utils.containerName(vars.image.repo, "${CI_COMMIT_SHA}"),
    script+: [
      "docker tag %s %s" % [vars.image.name, repo_with_sha],
      "docker push %s" % [repo_with_sha],
    ],
    only: ['branches'],
  },
}, stage=stages.docker_build);


local unit_tests = mergeJob(baseJob.unitTest, jobs={
  "unit-tests": {
    script: [
      "py.test --timeout=7200 --verbose --show-count ./ --color=no -x"] },

  "registry-tests": {
    script: [
      "py.test --timeout=7200 --verbose --show-count ./test/registry_tests.py --color=no -x"] },

  "karma-tests": {
    script: [
      "yarn test"] },
}, stage=stages.unit_tests);


local db_tests = mergeJob(baseJob.unitTest, jobs={
  local dbname = "quay",
  "postgres": baseJob.dbTest("postgresql",
                           image="postgres:9.6",
                           env={ POSTGRES_PASSWORD: dbname, POSTGRES_USER: dbname }),

  "mysql": baseJob.dbTest("mysql+pymysql",
                        image="mysql:latest",
                        env={ [key]: dbname for key in ["MYSQL_ROOT_PASSWORD", "MYSQL_DATABASE",
                                                        "MYSQL_USER", "MYSQL_PASSWORD"] }),

}, stage=stages.integration);


// build the gitlab-ci.yml:
{
  stages: stages_list,
  variables: vars.global,
} +
container_builds +
unit_tests +
db_tests
