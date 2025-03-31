{ networkx
, multimethod
, loguru
, icecream
, numpy
, rich
, multiset
, bidict
, poetry-core
, buildPythonPackage
}:

buildPythonPackage {
  pname = "spization";
  version = "0.0.1";
  src = ./.;

  propagatedBuildInputs = [
    networkx
    multimethod
    loguru
    icecream
    numpy
    rich
    multiset
    bidict
  ];

  build-system = [
    poetry-core
  ];
}
