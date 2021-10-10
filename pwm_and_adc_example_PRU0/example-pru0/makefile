# am335x processor - pru core 0

# to do
# - check if the core is already running before load the firmware, if the core is running, stop it and load
# - check if the core is shuted down and the firmware is loaded before start the core

# project directory
prj_dir = $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
# source files directory
src_dir = $(prj_dir)/source
# build files directoy
bld_dir = $(prj_dir)/build

# firmware directory
fmw_dir = /lib/firmware
# remoteproc (remote procesor) driver directory
rpd_dir = /sys/class/remoteproc/remoteproc1
# pru code generation tools directory
cgt_dir = /usr/share/ti/cgt-pru
# pru software support package directory
ssp_dir = /usr/lib/ti/pru-software-support-package

# project name
prj = $(notdir $(prj_dir))
# source files
src = $(wildcard $(src_dir)/*.c)
# object files
obj = $(patsubst $(src_dir)/%,$(bld_dir)/%,$(src:.c=.object))
# linker command file
lnk = $(wildcard $(src_dir)/*.cmd)
# out file
out = $(bld_dir)/$(prj).fw

# compiler flags
# pru-icss compiler user guide section 2.3
# clpru --help
c_flg = \
	--include_path=$(cgt_dir)/include \
	--include_path=$(ssp_dir)/include \
	--include_path=$(ssp_dir)/include/am335x \
	--display_error_number \
	--hardware_mac=on \

# linker flags
# pru-icss compiler user guide section 2.3.1
# clpru --run_linker --linker_help
l_flg = \
	--output_file=$(out) \
	--heap_size=0x100 \
	--stack_size=0x100 \
	--search_path=$(cgt_dir)/lib \
	--search_path=$(ssp_dir)/lib \
	--library=libc.a \
	--library=rpmsg_lib.lib \
	--reread_libs \
	--display_error_number \
	--warn_sections

.PHONY: all clean load

all: $(out)

# generates a out file using object files
$(out): $(obj) $(lnk)
	@echo ''
	@echo '  link $< to generate $@'
	@echo ' '
	clpru --run_linker --ram_model $< $(l_flg) $(lnk)
	@echo ' '

# generates object files using source files
$(obj): $(src)
	@echo ''
	@echo '  compile $<'
	@echo ' '
	@mkdir --parents $(bld_dir)
	clpru $(c_flg) --output_file=$@ $<
	@echo ' '

clean:
	@echo ''
	@echo '  $@ $(bld_dir) directory'
	@echo ''
	@if [ -d $(bld_dir) ]; then \
		rm --recursive --verbose $(bld_dir); \
	else \
		echo '$(bld_dir) directory does not exist, it is nothing to do here'; \
	fi
	@echo ''

load: $(out)
	@echo ""
	@echo " $@ $(out) to $(fmw_dir) "
	@echo ""
	cp $(out) $(fmw_dir)
	echo $(notdir $(out)) > $(rpd_dir)/firmware
	@echo ""

start:
	@echo ""
	@echo " $@ pru0 core"
	@echo ""
	echo "start" > $(rpd_dir)/state
	@echo""

stop:
	@echo ""
	@echo " $@ pru0 core"
	@echo ""
	echo "stop" > $(rpd_dir)/state
	@echo ""
