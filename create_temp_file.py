import os
import tempfile
import time

import sublime
import sublime_plugin

# Put a small starter snippet (e.g. hello world) in new files.
INSERT_TEMPLATE = False

# Folder (inside your OS temp directory) where the files are created.
TEMP_DIR_NAME = "sublime_temp_files"

# key: (display name, file extension, starter template)
LANGUAGES = {
    "python": ("Python", "py", r"""
print("Hello, world!")
"""),
    "javascript": ("JavaScript", "js", r"""
console.log("Hello, world!");
"""),
    "typescript": ("TypeScript", "ts", r"""
const message: string = "Hello, world!";
console.log(message);
"""),
    "java": ("Java", "java", r"""
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, world!");
    }
}
"""),
    "c": ("C", "c", r"""
#include <stdio.h>

int main(void) {
    printf("Hello, world!\n");
    return 0;
}
"""),
    "cpp": ("C++", "cpp", r"""
#include <iostream>

int main() {
    std::cout << "Hello, world!" << std::endl;
    return 0;
}
"""),
    "csharp": ("C#", "cs", r"""
using System;

class Program
{
    static void Main()
    {
        Console.WriteLine("Hello, world!");
    }
}
"""),
    "go": ("Go", "go", r"""
package main

import "fmt"

func main() {
    fmt.Println("Hello, world!")
}
"""),
    "rust": ("Rust", "rs", r"""
fn main() {
    println!("Hello, world!");
}
"""),
    "ruby": ("Ruby", "rb", r"""
puts "Hello, world!"
"""),
    "php": ("PHP", "php", r"""
<?php

echo "Hello, world!\n";
"""),
    "swift": ("Swift", "swift", r"""
print("Hello, world!")
"""),
    "kotlin": ("Kotlin", "kt", r"""
fun main() {
    println("Hello, world!")
}
"""),
    "scala": ("Scala", "scala", r"""
object Main extends App {
  println("Hello, world!")
}
"""),
    "dart": ("Dart", "dart", r"""
void main() {
  print('Hello, world!');
}
"""),
    "groovy": ("Groovy", "groovy", r"""
println "Hello, world!"
"""),
    "haskell": ("Haskell", "hs", r"""
main :: IO ()
main = putStrLn "Hello, world!"
"""),
    "elixir": ("Elixir", "exs", r"""
IO.puts("Hello, world!")
"""),
    "julia": ("Julia", "jl", r"""
println("Hello, world!")
"""),
    "lua": ("Lua", "lua", r"""
print("Hello, world!")
"""),
    "perl": ("Perl", "pl", r"""
use strict;
use warnings;

print "Hello, world!\n";
"""),
    "r": ("R", "R", r"""
cat("Hello, world!\n")
"""),
    "bash": ("Bash", "sh", r"""
#!/usr/bin/env bash

echo "Hello, world!"
"""),
    "powershell": ("PowerShell", "ps1", r"""
Write-Host "Hello, world!"
"""),
    "batch": ("Batch", "bat", r"""
@echo off
echo Hello, world!
"""),
    "sql": ("SQL", "sql", r"""
SELECT 'Hello, world!' AS message;
"""),
    "html": ("HTML", "html", r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>

</body>
</html>
"""),
    "css": ("CSS", "css", r"""
body {
    margin: 0;
}
"""),
    "json": ("JSON", "json", r"""
{

}
"""),
    "yaml": ("YAML", "yaml", ""),
    "xml": ("XML", "xml", r"""
<?xml version="1.0" encoding="UTF-8"?>
<root>

</root>
"""),
    "markdown": ("Markdown", "md", r"""
# Untitled
"""),
    "latex": ("LaTeX", "tex", r"""
\documentclass{article}

\begin{document}
Hello, world!
\end{document}
"""),
    "text": ("Plain Text", "txt", ""),
}


def _unique_path(folder, base, ext):
    path = os.path.join(folder, "{}.{}".format(base, ext))
    counter = 2
    while os.path.exists(path):
        path = os.path.join(folder, "{}_{}.{}".format(base, counter, ext))
        counter += 1
    return path


class CreateTempFileCommand(sublime_plugin.WindowCommand):
    def run(self, language=None):
        if language is None:
            self.choose_language()
        elif language in LANGUAGES:
            self.create(language)
        else:
            sublime.error_message(
                "Create Temp File: unknown language '{}'".format(language)
            )

    def choose_language(self):
        keys = sorted(LANGUAGES, key=lambda k: LANGUAGES[k][0].lower())
        items = [LANGUAGES[k][0] for k in keys]

        def on_select(index):
            if index >= 0:
                self.create(keys[index])

        self.window.show_quick_panel(items, on_select)

    def create(self, language):
        name, ext, template = LANGUAGES[language]
        root = os.path.join(tempfile.gettempdir(), TEMP_DIR_NAME)

        try:
            os.makedirs(root, exist_ok=True)

            if language == "java":
                folder = tempfile.mkdtemp(prefix="java_", dir=root)
                path = os.path.join(folder, "Main.java")
            else:
                stamp = time.strftime("%Y%m%d_%H%M%S")
                path = _unique_path(root, "temp_" + stamp, ext)

            content = ""
            if INSERT_TEMPLATE and template:
                content = template.strip("\n") + "\n"

            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
        except OSError as e:
            sublime.error_message("Create Temp File: could not create file\n\n{}".format(e))
            return

        view = self.window.open_file(path)
        view.set_status("temp_file", "Temp file")
