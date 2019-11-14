# website-data
Build production environment:
```
make install
```
Run development environment:
```
make develop
```
Run tests (make sure that the development environment is running):
```
make test
```

## Usage scenarios*
*curl package is required 
### Website content order
Run production/development environment.
Make an order:
```
curl --header "Content-Type: application/json" --data '{"website_url": "http://90minut.pl", "order_type": "content"}' http://localhost:5000/order_website
```
Use your order_id to check the order status:
```
curl http://localhost:5000/order_status/<order_id>
```
When the order is ready (finished) you can pickup the content:
```
curl http://localhost:5000/pickup_order/<order_id>
```
### Website images order
Run production/development environment.
Make an order:
```
curl --header "Content-Type: application/json" --data '{"website_url": "http://90minut.pl", "order_type": "images"}' http://localhost:5000/order_website
```
Use your order_id to check the order status:
```
curl http://localhost:5000/order_status/<order_id>
```
When the order is ready (finished) you can pickup the zipped images:
```
curl http://localhost:5000/pickup_order/<order_id> --output <output_path.zip>
```