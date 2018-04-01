# generate_find_module.py

## Descrition
A script to generate CMake Find Modules.

## Usage

```
./generate_find_module.py --name <module_name> --include <include_file_name> --lib <library_base_name> [--target <target_name>] [--package <package_name>] [--outdir <output_directory>]
```

**module\_name:** Name of the module to find. Examples: CURL, PCRE

**include\_file\_name:** Name of the include file to search for. Examples: curl.h, sqlite3.h, pcre.h

**library\_base\_name:** Name of the library file to search for. Examples: curl, sqlite3, pcre16

**target\_name:** Name of the imported target that will be created. Examples: CURL::CURL, PCRE::PCRE16

**package\_name:** Name of the package that will be passed to pkg-config (optional). Examples: libcurl, zlib, sqlite3

**outdir:** Output directory name.

## Case study

Let's assume you want to create a find module for CURL. First thing to do is to figure out if CMake provides a find module for this library. This is the case for CURL, but we found out that the find module cmake provides does not create an imported target, so we need to create our custom find module using generate\_find\_module.

For that, we need several pieces of informations:

* The name of the include file we need to search for. In this case, the filename is `curl.h`

* The name of the library we need to search for. For CURL, the library name is `libcurl.dylib` on macOS and `libcurl.so` on other unices. So the library name we need to pass te `generate_find_module.py` is `curl`.

* The name of the pkg-config package CURL provides. We can find out using the following command: ```pkg-config --list-all|grep -i curl``` . In this case, the name of the pkg-config package is `libcurl`

We now have enough information to generate a find module. Let's invoke the script:

```
./generate_find_module.py \
    --name CURL \
    --include curl.h \
    --lib curl \
    --target CURL::CURL \
    --package libcurl
```

This will generate a `FindCURL.cmake` in the current directory. Copy that file to your project's `CMAKE_MODULE_PATH` and add the following statement to your `CMakeLists.txt`:

```
find_library(CURL REQUIRED)
```

You can now link your target executable/library with the curl imported target:

```
target_link_libraries(${PROJECT_NAME} CURL::CURL)
```


