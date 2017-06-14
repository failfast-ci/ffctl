
{
  local topSelf = self,
    # Generate a sequence array from 1 to i
   seq(i):: (
      [x for x in std.range(1, i)]
   ),

  objectFieldsHidden(obj):: (
     std.setDiff(std.objectFieldsAll(obj), std.objectFields(obj))
  ),

  objectFlatten(obj):: (
    // Merge 1 level dict depth into toplevel
    local visible = {[k]: obj[j][k],
                    for j in std.objectFieldsAll(obj)
                    for k in std.objectFieldsAll(obj[j])};

    visible
  ),

   compact(array):: (
     [x for x in array if x != null]
   ),

   objectValues(obj):: (
     local fields =  std.objectFields(obj);
      [obj[key] for key in fields]
   ),

   objectMap(func, obj):: (
    local fields = std.objectFields(obj);
    {[key]: func(obj[key]) for key in fields}
    ),

   capitalize(str):: (
     std.char(std.codepoint(str[0]) - 32) + str[1:]
   ),

   test: self.capitalize("test"),

set(array)::
  { [key]: key for key in array },

containerName(repo, tag):: "%s:%s" % [repo, tag],

ci: {

mergeJob(base_job, jobs, stage=null):: {
  [job_name]: base_job + jobs[job_name] +
         if stage != null then {stage: stage} else {}
  for job_name in std.objectFields(jobs)
},

only(key):: (
  if key == "master"
  then { only: ['master', 'tags'] }
  else { only: ['branches'] }
),

setManual(key, values):: (
  if std.objectHas(topSelf.set(values), key)
  then { when: 'manual' }
  else { only: ['branches'] }
),
},
baseJob: {
dockerBuild: {
  // base job to manage containers (build / push)
  variables: {
    DOCKER_DRIVER: "aufs",
  },
  image: "docker:git",
  before_script: [
    "docker login -u $DOCKER_USER -p $DOCKER_PASS quay.io",
  ],
  services: [
    "docker:dind",
  ],
  tags: [
    "docker",
  ],
},

unitTest: {
  // base job to test the container
  variables: {
    GIT_STRATEGY: "none",
  },
  before_script: [
    "cd /",
    "source venv/bin/activate",
  ],
  tags: [
    "kubernetes",
  ],
},

dbTest(scheme, image, env):: self.unitTest + {
  variables+: {
    SKIP_DB_SCHEMA: 'true',
    TEST_DATABASE_URI: '%s://quay:quay@localhost/quay' % scheme,
  } + env,
  services: [image],
  script: [
      "sleep 30",
    "alembic upgrade head",
    'PYTHONPATH="." TEST="true" py.test --timeout=7200 --verbose --show-count ./ --color=no --ignore=endpoints/appr/test/ -x',
    ]
}
}}
