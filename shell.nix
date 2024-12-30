with import <nixpkgs> {};
let 
	setuptools = pkgs.python312Packages.buildPythonPackage {
		name = "setuptools";
		version = "61.0.0";
		pyproject = true;
		src = pkgs.fetchurl {
			url = "https://files.pythonhosted.org/packages/4d/5b/dc575711b6b8f2f866131a40d053e30e962e633b332acf7cd2c24843d83d/setuptools-69.2.0.tar.gz";
			sha256 = "sha256-D/QYP49CzY+jrOoWxFIFUhpO8o9zxjkdiiXpKJMTTy4=";
		};
	};
	django = pkgs.python312Packages.buildPythonPackage {
		name = "django";
		version = "5.1.2";
		pyproject = true;
		src = pkgs.fetchurl {
			url = "https://files.pythonhosted.org/packages/9c/e5/a06e20c963b280af4aa9432bc694fbdeb1c8df9e28c2ffd5fbb71c4b1bec/Django-5.1.2.tar.gz";
			sha256 = "sha256-vXN2+QyZ+WtkNyLu5nZJhwbJ/X3HWfVev68sCOvN9PA=";
		};
		build-system = [
			setuptools
		];
		dependencies = [
			pkgs.python312Packages.asgiref
			pkgs.python312Packages.sqlparse
		];
	};
in mkShell {
	packages = [
		(python312.withPackages (ps: [
			django
			ps.python-lsp-server
			ps.pylsp-mypy
			ps.pyls-isort
			ps.flake8
			ps.pylint
		]))
	];
	doCheck = false;
}
