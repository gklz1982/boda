# NOTE: see also the file obj_list in the project root.  

# NOTE_DETAILS: the build system for this project consists of this makefile, the python script
# pysrc/prebuild.py, and the file obj_list read by the python scripts. running make on this makefile is the
# correct top-level build command. however, note that configuring the project may require edits to this
# makefile, the obj_list file, and/or the python build scripts.

# --- makefile preliminary setup begins --- 
# the build should be run in a build directory named .obj under the project root with a symlink to the makefile. we check for this:
ifeq ($(shell test -L makefile ; echo $$? ),1)
all :   # if it doesn't look like we're in a build directory, assume we're at the project root, make one, and run make there.
	@echo "./makefile is not a symlink. creating ./obj,./lib,./run; symlinking to makefile in ./obj; running make in ./obj"
	mkdir -p obj run lib && ln -sf ../makefile obj/makefile && cd obj && $(MAKE)
else
$(info py_prebuild_rm_okay: $(shell rm -f prebuild.okay ))
# run python build code: generates various code, object list file, and dependency list file
# FIXME: make seems to somtimes like to run prebuild.py multiple times -- which is not great, but okay.
$(info py_prebuild_hook:  $(shell python ../pysrc/prebuild.py )) # creates an empty prebuild.okay file on success
ifeq ($(shell test -f prebuild.okay ; echo $$? ),1)
$(error "prebuild.okay file does not exist. assuming prebuild.py failed, aborting make")
endif
# --- makefile preliminary setup ends ---
# --- makefile header section begins --- 
# edit paths / project info / configuration here
TARGET := ../lib/boda
#LIBTARGET=../lib/libboda.so # currently unused/broken for boda, enabling may be usefull for pre-debugging/testing shared-lib building 
CPP := g++
CPPFLAGS := -Wall -O3 -g -std=c++0x -rdynamic -fPIC -fopenmp -Wall 
LDFLAGS := -lboost_system -lboost_filesystem -lboost_iostreams -lboost_regex -lpython2.7 -fopenmp 
include dependencies.make
# --- makefile header section ends --- 
# --- makefile generic c++ compilation, linking, and dependency handling rules and reciepies section begins --- 
# generally, there is no need to alter the makefile below this line
VPATH := ../src ../src/gen ../src/ext
OBJS := $(shell cat gen_objs)
.SUFFIXES:
%.o : %.cc
	$(CPP) $(CPPFLAGS) -MMD -c $<
%.d : %.cc
	rm -f $(@:.d=.o)
%.o : %.cpp
	$(CPP) $(CPPFLAGS) -MMD -c $<
%.d : %.cpp
	rm -f $(@:.d=.o)
DEPENDENCIES = $(OBJS:.o=.d)
all : $(TARGET) # $(LIBTARGET)
$(TARGET): $(OBJS) ../obj_list
	$(CPP) $(CPPFLAGS) -o $(TARGET) $(OBJS) $(LDFLAGS)
$(LIBTARGET): $(OBJS)
	$(CPP) -shared $(CPPFLAGS) -o $(LIBTARGET) $(OBJS) $(LDFLAGS)
.PHONY : clean
clean:
	-rm -f $(TARGET) $(OBJS) $(DEPENDENCIES)
include $(DEPENDENCIES)
include make_make_ignore_missing_headers_in_d_files.make # generated by prebuild.py
# --- makefile generic c++ compilation, linking, and dependency handling rules and reciepies section ends --- 
endif
