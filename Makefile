S3_BUCKET = s3://docs.makingwithcode.org/retro
CF_DISTRIBUTION = EPA6NHZ2LEH1A

.PHONY: build deploy clean

build:
	$(MAKE) -C documentation html

deploy: build
	aws s3 sync documentation/build/html $(S3_BUCKET)
	aws cloudfront create-invalidation --distribution-id $(CF_DISTRIBUTION) --paths "/retro/*"

clean:
	$(MAKE) -C documentation clean
