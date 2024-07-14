FROM dunglas/frankenphp

COPY . /app/public

# add additional extensions here:
RUN install-php-extensions \
	pdo_mysql \
	gd \
	intl \
	zip \
	opcache