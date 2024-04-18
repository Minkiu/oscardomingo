---
layout: post.html
title: Setting up Notea with Minio
tags: [docker, docker-compose, notea, minio, note-taking, vps, self-host]
---
In this tutorial we’ll be setting up **Notea** (<https://cinwell.com/notea/>) with **Minio** (<https://github.com/minio/minio>) for it’s storage, since the former requires a S3 compatible storage, I started with this guide over at CyberHost <https://cyberhost.uk/notea/> and changed it to my liking while updating certain bits that have changed since.

## Docker Compose

We’ll use `docker-compose`, to install it head to <https://docs.docker.com/compose/install/>, to orchestrate the two services, so let’s create a folder for our project and create a `docker-compose.yaml` file:


```
mkdir notea && cd notea && touch docker-compose.yaml
```

Now with your favorite editor add the following and replace the <code>&lt;values&gt;</code> with the correct information:

```
version: '3'
services:
    notea:
      image: cinwell/notea
      container_name: notea
      environment:
        - STORE_ACCESS_KEY=<minio-user>
        - STORE_SECRET_KEY=<minio-password>
        - STORE_BUCKET=notea
        - STORE_END_POINT=https://<minio.your.domain>
        - STORE_FORCE_PATH_STYLE=true
        - PASSWORD=<notea-password>
        - COOKIE_SECURE=true
        - BASE_URL=https://<notea.your.domain>
      ports:
        - "3000:3000"
    notea-s3:
      image: minio/minio
      container_name: notea-s3
      environment:
        MINIO_ROOT_USER: <minio-user>
        MINIO_ROOT_PASSWORD: <minio-password>
      ports:
        - "9000:9000"
      volumes:
        - /data/notea:/data
      entrypoint: sh
      command: -c 'mkdir -p /data/notea && /usr/bin/minio server /data'
```

 If you don't care where the data (the notes) lives within your host, for backing up reasons, you could use a docker named volume:


```
     notea-s3:
			...
      volumes:
        - notea-volume:/data
      ...
```

<div class="warn-note">
	From now on, all commands will require <b>sudo</b>.
</div>

Then we build `up` the containers and start them `-d`etached (in the background):

```
docker-compose up -d
```

We can check that everything is nominal by:

```
docker-compose ps
```

And if you want to check the logs of one of the containers you can:

```
docker-compose logs <container_name>
```

If you want to stop them you can do so with:

```
docker-compose stop
```

And if you want to start from scratch you can do:


<div class="danger-note">
	This removes all the data associated with our docker-compose, if you used a named volume, you will lose your notes.
</div>


```
docker-compose down
```

## Nginx (Reverse Proxy)

Now we need to tell our server to return our notea and minio instance when it receives a request to certain url, for this task I use `nginx` , to install it head to <https://www.nginx.com/resources/wiki/start/topics/tutorials/install/>, with your favorite editor open `/etc/nginx/sites-available/your.domain` (depending of your distro, this folder might not exist and it’s `/etc/nginx/sites-enabled/your.domain` for more <https://stackoverflow.com/a/17415606/1987581> ) and add:

```
server {
	server_name <notea.your.domain>;
	location / {
		proxy_pass http://0.0.0.0:3000;
	}

}

server {
	# Change to your URL, has to match the one in `docker-compose.yaml`
	server_name <minio.your.domain>;

	# Settings from: https://docs.min.io/docs/setup-nginx-proxy-with-minio.html

	# To allow special characters in headers
	ignore_invalid_headers off;

	# Allow any size file to be uploaded.
	# Set to a value such as 1000m;
	# to restrict file size to a specific value
	client_max_body_size 0;

	# To disable buffering
	proxy_buffering off;

	location / {
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Proto $scheme;
		proxy_set_header Host $http_host;

		proxy_connect_timeout 300;
		# Default is HTTP/1, keepalive is only enabled in HTTP/1.1
		proxy_http_version 1.1;
		proxy_set_header Connection "";
		chunked_transfer_encoding off;
		proxy_pass http://0.0.0.0:9000;
	}

}


server {
	server_name <minio.your.domain>;
	listen 80;

}

server {
	server_name <notea.your.domain>;
	listen 80;

}
```

Let’s test our config with:

```
nginx -t
```

We now make sure we got SSL certificate ( `https` ) for our site with the handy `certbot` utility, to install it head to <https://certbot.eff.org/instructions> :

```
certbot --nginx
```

Follow the instructions and enable it for both `<notea.your.domain>` and `<minio.your.domain>` and apply the redirections.

Now we need to restart the `nginx` service, in a `systemd` server:

```
systemctl restart nginx
```

I like to check the status after a restart to make sure everything is fine:

```
systemctl status nginx
```

## Notea

Now when visiting `<notea.your.domain>` you should be greeted by a password input, use `<notea-password>` and you should now be good to go!


<div class="info-note">
	Remember to keep these <code>&lt;values&gt;</code> safe in a password manager and remove them from the file in the server, I change them to <code>redacted</code> but you can put whatever feels right.
</div>


## Updates

I normally subscribe to new releases on GitHub, <https://github.com/QingWei-Li/notea>, to know when to restart and get the latest version:

```
docker-compose stop
```

```
docker-compose pull
```

```
docker-compose up -d
```

Don’t forget that you can report bugs, suggest features and/or contribute.

That’s all, happy note taking!