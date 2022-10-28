 upstream parser_hackaton{
	 server django:8000;
}


server {
	listen 80;
	server_name  parser_hackatons;
	location /static/ {
		alias /server/staticfiles/;
	}

	location / {
	    	proxy_pass   http://parser_hackaton;
    		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
   		proxy_set_header Host $host;
   		proxy_redirect off;
	}

}

