
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
docker: {
    login(user, pass, registry):: "docker login -u %s -p %s %s" % [user, pass, registry],
},

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

}
