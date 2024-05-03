+++
title = "Installing Maya on a Rocky Linux 9 container"
date = 2024-05-03
+++

I've recently crafted a `dockerfile` which will install Maya in an OCI compatible Rocky Linux 9.2 image, which then can be used to create `distrobox` (or `toolbx`) compatible containers, on the process I've learned a couple of "tricks" when it comes to debugging what a binary needs in order to work.

As of this writing, the runtime packages needed to run Maya 2024 are the following:

```
libpng libjpeg libtiff freetype libXpm libXi fontconfig libXinerama alsa-lib libXcomposite libXdamage libXrandr libXrender libXtst libxcrypt-compat libxkbcommon nspr nss nss-util pciutils-libs libnsl xcb-util-wm xcb-util-image xcb-util-image xcb-util-renderutil libxkbcommon-x11 libmng libXcursor
```

Historically, whenever I faced this situation, after installing the officially specified packages from the Maya Help page and still not getting it to launch (???), I would be running `maya` , note whatever `.so` failed to load, do a `dnf provides <library-name>.so`, then installing the package that had it, rinse and repeat.

Well that is not fun isn't it? (Maybe the first time you do it yes, but when you had had to do this for the `n`th time you start wondering why Autodesk likes to punish their users this way).

So some shortcuts I discovered this time around are `ldd` and `QT_DEBUG_PLUGINS=1`, I knew about the former, but never clicked that it would work for this, is you run:
`ldd /path/to/maya.bin` notice the `bin` which is the actual binary run after some round trips following symbolic links and the python file that sets up some environment variables.

If we chain it with grep: `ldd /path/to/maya.bin | grep not` we'll get a list of all missing libraries in our system, example:

```
ldd /usr/autodesk/maya2024/bin/maya.bin  | grep "not found"
	libcrypt.so.1 => not found
	libsmime3.so => not found
	libnss3.so => not found
	libnssutil3.so => not found
	libplds4.so => not found
	libplc4.so => not found
	libnspr4.so => not found
	libXcomposite.so.1 => not found
	libXdamage.so.1 => not found
	libXrender.so.1 => not found
	libXrandr.so.2 => not found
	libXtst.so.6 => not found
	libxkbcommon.so.0 => not found
	libpci.so.3 => not found
	libasound.so.2 => not found
```

You can then come out with a list to pass to `dnf provides`, such as:

```
dnf provides libcrypt.so.1 libsmime3.so libnss3.so libnssutil3.so libplds4.so libplc4.so libnspr4.so libXcomposite.so.1 libXdamage.so.1 libXrender.so.1 libXrandr.so.2 libXtst.so.6 libxkbcommon.so.0 libpci.so.3 libasound.so.2
```

And then install every package that shows up in that command, pretty sure all this could be automated with either a `python` script or some ~~mad~~ brilliant bash one liner.

Anyhow, we got all the things we need to launch maya, right? Right? I guess it would be too easy on IT/Pipe devs so once you launch you'll be greeted with the infamous:

```
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: linuxfb, minimal, offscreen, vnc, xcb.
```

Okay, what now then... you can google that, and chances is you'll end up installing a package that does fix it, but in the effort of keeping the `image` as slim as possible, I just want to install what's absolutely necessary for me to open maya, debug whatever esoteric self-inflicted issue, fix it, close it and hopefully never have to open it again (hah).

Enter `QT_DEBUG_PLUGINS=1 maya` , [credit to this SO answer](https://stackoverflow.com/a/76213596), this will dump a lot of `Qt` related information and errors, we can use grep again such as: `QT_DEBUG_PLUGINS=1 maya | grep cannot` which will provide us again a list of `x11` related libraries we need to install in order to get `maya` to open.

There you have it, go and push some pixels; in an ideal world, Autodesk would have caught up by now with better ways to [distribute their Linux software](https://forums.autodesk.com/t5/maya-ideas/appimage-flatpak-or-snap-for-linux/idi-p/9235510) (please vote if you can?) or maybe declare the dependencies on their `rpms` (even tho vendored `tcl` and `tk` conflict with what you get when installing with `dnf` so go figure) but for the time being we'll left to suffer.

I'll be that guy and tell you to push for [Blender](https://www.blender.org/) at your company, and if they can donate or contribute back the better :)
