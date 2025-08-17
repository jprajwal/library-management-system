with import <nixpkgs> {};
let 
	setuptools = pkgs.python312Packages.buildPythonPackage {
		name = "setuptools";
		version = "69.0.0";
		pyproject = true;
		src = pkgs.fetchurl {
			url = "https://files.pythonhosted.org/packages/91/43/4121cf96ed3a2d68d862663552d8044e1d987d716b6a065ab53cd4d4640f/setuptools-69.0.0.tar.gz";
			sha256 = "sha256-TGXU94keWwRukUaRO4cJgUTeLKISj7wQE1uFVqbd2UY=";
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
	django-extensions = pkgs.python312Packages.buildPythonPackage {
		name = "django-extensions";
		version = "3.2.3";
		pyproject = true;
		src = pkgs.fetchurl {
			url = "https://github.com/django-extensions/django-extensions/archive/refs/tags/3.2.3.tar.gz";
			sha256 = "sha256-xw1nJxtzpFxlFcpUsQvwk2EDVzCopgNsyggh+zD5/9o=";
		};
		build-system = [
			setuptools
		];
		dependencies = [
			django
		];
	};
in mkShell {
	packages = [
		(python312.withPackages (ps: [
			django
			django-extensions
			ps.python-lsp-server
			ps.pylsp-mypy
			ps.pyls-isort
			ps.flake8
			ps.pylint
		]))
	];
	doCheck = false;
}
