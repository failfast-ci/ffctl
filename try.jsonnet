local parent = {top: {
    sub: {a: 1, b:2},
    },
};

local tryMerge(path, partial=false) = (
   local patch = {sub+: {c: 3}};

   if partial then patch else path(patch)
);
local patch = {sub+: {c: 3}};
parent + tryMerge(function(patch){top+: patch})
// parent + tryMerge({top: {sub: {}}},)
//+ ({top+: parent.top + tryMerge(true)})

// service + Service.Spec.mergePorts([5040]) // add port (works for dict) {spec+: {port+: ...}},
// service + Service.Spec.addPorts([5040]) // add port (works for array) {spec+: {port+: ...}},
// service + Service.Spec.Ports([5040]) // replace all ports {spec+: {port: ...}},
// service + Service.Spec.setPorts([5040]) // replace all ports {spec+: {port: ...}},

// service.spec + Service.Spec.mergePorts([5040], partial=true) // add port {port+: ...},
// service.spec.ports + Service.Spec.Ports([5040]).ports
