FROM ubuntu:22.04


RUN apt-get update -y && apt-get upgrade -y
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
RUN apt update; apt install -y python build-essential git git-lfs subversion cmake libx11-dev libxxf86vm-dev libxcursor-dev libxi-dev libxrandr-dev libxinerama-dev libegl-dev; apt install libwayland-dev wayland-protocols libxkbcommon-dev libdbus-1-dev linux-libc-dev

RUN apt-get install -y python3 git-all python3-pip git-lfs
RUN pip install --no-cache nvidia-tensorrt --index-url https://pypi.ngc.nvidia.com


# Downloads to user config dir
ADD https://ultralytics.com/assets/Arial.ttf https://ultralytics.com/assets/Arial.Unicode.ttf /root/.config/Ultralytics/

# Install linux packages
# g++ required to build 'tflite_support' and 'lap' packages, libusb-1.0-0 required for 'tflite_support' package
RUN apt update \
    && apt install --no-install-recommends -y gcc git cmake make git libgtk2.0-dev pkg-config zip curl htop libgl1-mesa-glx libglib2.0-0 libpython3-dev gnupg g++ libusb-1.0-0
RUN alias python=python3

WORKDIR /app


RUN mkdir ~/blender-git; cd ~/blender-git; git clone https://projects.blender.org/blender/blender.git;

RUN cd ./bleder; build_files/utils/make_update.py --use-linux-libraries
RUN cmake -C ./build_files/cmake/config/bpy_module.cmake /app/blender
RUN python3 ./build_files/utils/make_bpy_wheel.py /app/build_bpy/bin/ && pip3 install bpy-{version-and-platform}.whl


