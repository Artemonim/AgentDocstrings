"""Shared pytest configuration and fixtures for Agent Docstrings tests."""

from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Iterator, Dict

import pytest


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    """Returns the absolute path to the *fixtures* directory used in tests."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture()
def sample_python_file(tmp_path: Path) -> Iterator[Path]:
    """Creates a simple temporary Python file and yields its path.

    The temporary file is removed automatically when the test finishes.
    """
    code = textwrap.dedent(
        """
        class Foo:
            def bar(self, x):
                return x

        def baz(y):
            return y * 2
        """
    ).lstrip()

    file_path = tmp_path / "sample.py"
    file_path.write_text(code, encoding="utf-8")
    yield file_path


@pytest.fixture()
def sample_kotlin_file(tmp_path: Path) -> Iterator[Path]:
    """Creates a temporary Kotlin file for testing."""
    code = textwrap.dedent(
        """
        class MainActivity {
            fun onCreate() {
                println("Hello")
            }
            
            private fun helper(): String {
                return "help"
            }
        }
        
        fun globalFunction(param: String): Int {
            return param.length
        }
        """
    ).lstrip()

    file_path = tmp_path / "sample.kt"
    file_path.write_text(code, encoding="utf-8")
    yield file_path


@pytest.fixture()
def sample_javascript_file(tmp_path: Path) -> Iterator[Path]:
    """Creates a temporary JavaScript file for testing."""
    code = textwrap.dedent(
        """
        class Calculator {
            constructor() {
                this.value = 0;
            }
            
            add(num) {
                this.value += num;
                return this;
            }
            
            get result() {
                return this.value;
            }
        }
        
        function globalSum(a, b) {
            return a + b;
        }
        
        export { Calculator, globalSum };
        """
    ).lstrip()

    file_path = tmp_path / "sample.js"
    file_path.write_text(code, encoding="utf-8")
    yield file_path


@pytest.fixture()
def sample_typescript_file(tmp_path: Path) -> Iterator[Path]:
    """Creates a temporary TypeScript file for testing."""
    code = textwrap.dedent(
        """
        interface User {
            name: string;
            age: number;
        }
        
        class UserService {
            private users: User[] = [];
            
            addUser(user: User): void {
                this.users.push(user);
            }
            
            getUsers(): User[] {
                return this.users;
            }
        }
        
        function createUser(name: string, age: number): User {
            return { name, age };
        }
        
        export { UserService, createUser, User };
        """
    ).lstrip()

    file_path = tmp_path / "sample.ts"
    file_path.write_text(code, encoding="utf-8")
    yield file_path


@pytest.fixture()
def sample_csharp_file(tmp_path: Path) -> Iterator[Path]:
    """Creates a temporary C# file for testing."""
    code = textwrap.dedent(
        """
        using System;
        
        public class Calculator
        {
            private int value;
            
            public Calculator()
            {
                value = 0;
            }
            
            public int Add(int number)
            {
                value += number;
                return value;
            }
            
            public void Reset()
            {
                value = 0;
            }
        }
        
        public static class MathUtils
        {
            public static int Multiply(int a, int b)
            {
                return a * b;
            }
        }
        """
    ).lstrip()

    file_path = tmp_path / "sample.cs"
    file_path.write_text(code, encoding="utf-8")
    yield file_path


@pytest.fixture()
def sample_cpp_file(tmp_path: Path) -> Iterator[Path]:
    """Creates a temporary C++ file for testing."""
    code = textwrap.dedent(
        """
        #include <iostream>
        #include <string>
        
        class Person {
        private:
            std::string name;
            int age;
            
        public:
            Person(const std::string& n, int a);
            virtual ~Person();
            
            std::string getName() const;
            void setAge(int a);
            virtual void speak();
        };
        
        Person::Person(const std::string& n, int a) : name(n), age(a) {}
        
        Person::~Person() {}
        
        std::string Person::getName() const {
            return name;
        }
        
        void Person::setAge(int a) {
            age = a;
        }
        
        void Person::speak() {
            std::cout << "Hello, I'm " << name << std::endl;
        }
        
        int main() {
            Person p("John", 25);
            p.speak();
            return 0;
        }
        """
    ).lstrip()

    file_path = tmp_path / "sample.cpp"
    file_path.write_text(code, encoding="utf-8")
    yield file_path


@pytest.fixture()
def complex_python_file(tmp_path: Path) -> Iterator[Path]:
    """Creates a complex Python file with multiple classes, nested classes, and functions."""
    code = textwrap.dedent(
        """
        #!/usr/bin/env python3
        \"\"\"A complex Python module for testing.\"\"\"
        
        import typing
        from dataclasses import dataclass
        
        # * Module-level constants
        VERSION = "1.0.0"
        DEBUG = True
        
        
        @dataclass
        class Config:
            \"\"\"Configuration class.\"\"\"
            host: str = "localhost"
            port: int = 8080
            
            def get_url(self) -> str:
                return f"http://{self.host}:{self.port}"
        
        
        class DatabaseManager:
            \"\"\"Handles database operations.\"\"\"
            
            def __init__(self, config: Config):
                self.config = config
                self._connection = None
                
            def connect(self) -> bool:
                \"\"\"Establish database connection.\"\"\"
                # * Implementation details...
                return True
                
            def disconnect(self) -> None:
                \"\"\"Close database connection.\"\"\"
                if self._connection:
                    self._connection.close()
                    
            class Transaction:
                \"\"\"Inner class for transaction handling.\"\"\"
                
                def __init__(self, db_manager):
                    self.db_manager = db_manager
                    
                def begin(self) -> None:
                    \"\"\"Start transaction.\"\"\"
                    pass
                    
                def commit(self) -> None:
                    \"\"\"Commit transaction.\"\"\"
                    pass
                    
                def rollback(self) -> None:
                    \"\"\"Rollback transaction.\"\"\"
                    pass
        
        
        class UserService(DatabaseManager):
            \"\"\"Service for user operations.\"\"\"
            
            def create_user(self, name: str, email: str) -> int:
                \"\"\"Create a new user.\"\"\"
                # * Implementation...
                return 1
                
            def get_user(self, user_id: int) -> dict:
                \"\"\"Retrieve user by ID.\"\"\"
                return {"id": user_id, "name": "Test"}
                
            async def async_operation(self) -> typing.Any:
                \"\"\"An async method.\"\"\"
                return None
        
        
        def helper_function(data: typing.List[str]) -> typing.Dict[str, int]:
            \"\"\"Helper function for processing data.\"\"\"
            return {item: len(item) for item in data}
        
        
        def main() -> None:
            \"\"\"Main entry point.\"\"\"
            config = Config()
            service = UserService(config)
            service.connect()
            
            try:
                user_id = service.create_user("John Doe", "john@example.com")
                user = service.get_user(user_id)
                print(f"Created user: {user}")
            finally:
                service.disconnect()
        
        
        if __name__ == "__main__":
            main()
        """
    ).lstrip()

    file_path = tmp_path / "complex_sample.py"
    file_path.write_text(code, encoding="utf-8")
    yield file_path


@pytest.fixture()
def python_file_with_existing_header(tmp_path: Path) -> Iterator[Path]:
    """Creates a Python file that already has a docstring header."""
    code = textwrap.dedent(
        '''
        """
            Classes/Functions:
              - OldClass (line 8):
                - old_method(self) (line 9)
              - Functions:
                - old_function() (line 13)
        """
        class NewClass:
            def new_method(self):
                return "new"
        
        def new_function():
            return "updated"
        '''
    ).lstrip()

    file_path = tmp_path / "with_header.py"
    file_path.write_text(code, encoding="utf-8")
    yield file_path


@pytest.fixture()
def multilanguage_project(tmp_path: Path) -> Iterator[Path]:
    """Creates a project directory with files in multiple supported languages."""
    project_dir = tmp_path / "multilang_project"
    project_dir.mkdir()
    
    # * Create subdirectories
    (project_dir / "src").mkdir()
    (project_dir / "test").mkdir()
    (project_dir / "scripts").mkdir()
    
    # * Python files
    (project_dir / "src" / "main.py").write_text("class App:\n    def run(self):\n        pass")
    (project_dir / "test" / "test_main.py").write_text("def test_app():\n    pass")
    
    # * JavaScript files
    (project_dir / "src" / "utils.js").write_text("class Utils {\n    static format(s) { return s; }\n}")
    
    # * TypeScript files
    (project_dir / "src" / "types.ts").write_text("interface IUser { name: string; }")
    
    # * C# files
    (project_dir / "src" / "Service.cs").write_text("public class Service {\n  public void DoWork() {}\n}")
    
    # * C++ files
    (project_dir / "src" / "engine.cpp").write_text("class Engine {\npublic:\n  void start();\n};")
    
    # * Kotlin files
    (project_dir / "src" / "Activity.kt").write_text("class MainActivity {\n  fun onCreate() {}\n}")
    
    # * Non-source files (should be ignored)
    (project_dir / "README.md").write_text("# Project")
    (project_dir / "config.json").write_text('{"key": "value"}')
    
    yield project_dir


@pytest.fixture()
def empty_files_project(tmp_path: Path) -> Iterator[Path]:
    """Creates a project with empty or nearly empty files."""
    project_dir = tmp_path / "empty_project"
    project_dir.mkdir()
    
    # * Completely empty files
    (project_dir / "empty.py").write_text("")
    (project_dir / "empty.js").write_text("")
    
    # * Files with only comments/whitespace
    (project_dir / "comments_only.py").write_text("# Just a comment\n# Another comment\n\n")
    (project_dir / "whitespace.py").write_text("   \n\t\n  \n")
    
    # * Files with only imports/constants
    (project_dir / "imports_only.py").write_text("import os\nimport sys\n\nVERSION = '1.0'\n")
    
    yield project_dir


@pytest.fixture()
def sample_files_by_language(tmp_path: Path) -> Iterator[Dict[str, Path]]:
    """Creates sample files for all supported languages and returns a mapping."""
    files = {}
    
    # * Python
    files["python"] = tmp_path / "test.py"
    files["python"].write_text("class PyClass:\n    def method(self): pass\ndef py_func(): pass")
    
    # * Kotlin
    files["kotlin"] = tmp_path / "test.kt"
    files["kotlin"].write_text("class KtClass {\n    fun method() {}\n}\nfun ktFunc() {}")
    
    # * JavaScript
    files["javascript"] = tmp_path / "test.js"
    files["javascript"].write_text("class JsClass {\n    method() {}\n}\nfunction jsFunc() {}")
    
    # * TypeScript
    files["typescript"] = tmp_path / "test.ts"
    files["typescript"].write_text("class TsClass {\n    method(): void {}\n}\nfunction tsFunc(): void {}")
    
    # * C#
    files["csharp"] = tmp_path / "test.cs"
    files["csharp"].write_text("public class CsClass {\n    public void Method() {}\n}")
    
    # * C++
    files["cpp"] = tmp_path / "test.cpp"
    files["cpp"].write_text("class CppClass {\npublic:\n    void method();\n};")
    
    yield files


@pytest.fixture()
def malformed_files_project(tmp_path: Path) -> Iterator[Path]:
    """Creates a project with malformed source files for error handling tests."""
    project_dir = tmp_path / "malformed_project"
    project_dir.mkdir()
    
    # * Python with syntax errors
    (project_dir / "broken.py").write_text("class BrokenClass\n    def method(\n        return")
    
    # * JavaScript with incomplete syntax
    (project_dir / "broken.js").write_text("class BrokenClass {\n    method(\n}")
    
    # * C++ with incomplete declarations
    (project_dir / "broken.cpp").write_text("class BrokenClass {\npublic\n    void method(")
    
    # * Files with encoding issues (simulate with unusual content)
    (project_dir / "encoding_test.py").write_text("# -*- coding: latin-1 -*-\ndef función(): pass", encoding='utf-8')
    
    yield project_dir 