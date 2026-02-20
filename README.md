## Setup

Please install poetry and uv to the run the project.

```bash
uv sync
Poetry shell
```



Please set the OPENAI_API_KEY before running the code


### Data: 
Data cleanup is required and currently the following is handled


- gs://amt-creator-media-cache/instagram/posts/post-pics/3682419129890575942.jpg
- gc://amt-creator-media-cache/instagram/posts/post-pics/3682419129890575942.jpg


### Searching the data is done using the search.py file. Since I have indexed 2 users, I am displaying only the first user.
```bash
python src/search.py --query "Female creators, aged 18-30 who are interested in beauty products, specifically hair-care products"

Result 1:
  ID: celestialjojo
  Document: celestialjojo
  Metadata: {'platform': 'instagram', 'username': 'celestialjojo'}
  Distance: 1.0037
```

### Result interpretation:

I checked celestialjojo's image: [Image 1](https://storage.googleapis.com/amt-creator-media-cache/instagram/posts/post-pics/3682419129890575942.jpg)

Comparing that with the second result: [Image 2](https://storage.googleapis.com/amt-creator-media-cache/instagram/posts/post-pics/3718700956449060222.jpg)

It makes sense that celestialjojo is more relevant to the query.


## Please skip the indexing step as I have indexed 2 users and 10 images per user.
### Indexing the data is done using the indexer.py file. 
```bash
python src/indexer.py
```
It will print like the following:
```bash
Adding user celestialjojo with platform instagram and combined 10 embeddings
Adding user angela_gargano with platform instagram and combined 10 embeddings
Index saved to chroma_db
Indexed data
```

Improvements if I had 30 minutes more:
- If I had more time I would improvise the indexing process by parallelizing the indexing process.
- Currently I am using openai embedding model which is an unnecessary call, I would use Hugging Face embedding model that uses sentence-transformers library.
- I would create a http endpoint for searching the creators based on the user query.



