{ networkx
, multimethod
, loguru
, icecream
, numpy
, rich
, multiset
, bidict
, sage
, setuptools
, wheel
, pythonRelaxDepsHook
, buildPythonPackage
, pytest
}:

buildPythonPackage {
  pname = "spization";
  version = "0.0.1";
  src = ./.;
  pyproject = true;

  propagatedBuildInputs = [
    networkx
    multimethod
    loguru
    icecream
    numpy
    rich
    multiset
    bidict
    sage
  ];

  nativeBuildInputs = [
    pythonRelaxDepsHook
  ];

  nativeCheckInputs = [
    pytest
  ];

  pythonRelaxDeps = [
    "multimethod"
  ];

  pythonRemoveDeps = [
    "passagemath-graphs"
  ];

  build-system = [
    setuptools
    wheel
  ];
}
