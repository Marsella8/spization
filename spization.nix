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
, pytest
, mypy
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

  nativeCheckInputs = [
    pytest
    mypy
  ];

  build-system = [
    poetry-core
  ];
}
