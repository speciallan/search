# search

# scrapy
scrapy crawl content


# web api

分类列表
/category
/category/{page}

商品列表

GET /product/list
GET /product/list/{cid}/{page}

单个商品销量曲线

GET /product/date/{product_id}

单个商品情感分析

GET /product/emotion/{product_id}

评论列表

GET /comment/{product_id}/{level}/{page}

level [a/l/s/h] 分别代表所有、差评、中评、好评

商品搜索

POST /search/product/

参数 keywords / cate_id / brand / price_min / price_max
 / order[comment_asc/comment_desc/sale_asc/sale_desc/price_asc/price_desc]

评论搜索

GET /search/comment/{keywords}/{page}
