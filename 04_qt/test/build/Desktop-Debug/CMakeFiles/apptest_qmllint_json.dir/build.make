# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 4.0

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/tenshi/sync/code_sync/ist/qt/test

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/tenshi/sync/code_sync/ist/qt/test/build/Desktop-Debug

# Utility rule file for apptest_qmllint_json.

# Include any custom commands dependencies for this target.
include CMakeFiles/apptest_qmllint_json.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/apptest_qmllint_json.dir/progress.make

CMakeFiles/apptest_qmllint_json: /usr/lib/qt6/bin/qmllint
CMakeFiles/apptest_qmllint_json: /home/tenshi/sync/code_sync/ist/qt/test/Main.qml
CMakeFiles/apptest_qmllint_json: .rcc/qmllint/apptest_json.rsp
	cd /home/tenshi/sync/code_sync/ist/qt/test && /usr/lib/qt6/bin/qmllint @/home/tenshi/sync/code_sync/ist/qt/test/build/Desktop-Debug/.rcc/qmllint/apptest_json.rsp

CMakeFiles/apptest_qmllint_json.dir/codegen:
.PHONY : CMakeFiles/apptest_qmllint_json.dir/codegen

apptest_qmllint_json: CMakeFiles/apptest_qmllint_json
apptest_qmllint_json: CMakeFiles/apptest_qmllint_json.dir/build.make
.PHONY : apptest_qmllint_json

# Rule to build all files generated by this target.
CMakeFiles/apptest_qmllint_json.dir/build: apptest_qmllint_json
.PHONY : CMakeFiles/apptest_qmllint_json.dir/build

CMakeFiles/apptest_qmllint_json.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/apptest_qmllint_json.dir/cmake_clean.cmake
.PHONY : CMakeFiles/apptest_qmllint_json.dir/clean

CMakeFiles/apptest_qmllint_json.dir/depend:
	cd /home/tenshi/sync/code_sync/ist/qt/test/build/Desktop-Debug && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/tenshi/sync/code_sync/ist/qt/test /home/tenshi/sync/code_sync/ist/qt/test /home/tenshi/sync/code_sync/ist/qt/test/build/Desktop-Debug /home/tenshi/sync/code_sync/ist/qt/test/build/Desktop-Debug /home/tenshi/sync/code_sync/ist/qt/test/build/Desktop-Debug/CMakeFiles/apptest_qmllint_json.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : CMakeFiles/apptest_qmllint_json.dir/depend

