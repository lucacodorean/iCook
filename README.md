
# iCook

iCook is generative AI solution based on DistilGPT2, that enables its users to generate cooking recipes based on the ingredients they have in their house.

The model has been fine-tuned using RecipeNGL dataset available at https://www.kaggle.com/datasets/paultimothymooney/recipenlg. In the latest version, the fine-tuned model has been trained on a small portion of the entire dataset, that counts approximatively 50.000 entries, on 10 epochs. 

The current state of the model is *proof of concept*.


## Features

- Generate multiple recipes and keep them saved until session is refreshed.
- API endpoint that can be used for different FEs.


## Run Locally

Clone the project

```bash
  git clone https://github.com/lucacodorean/iCook
```

Go to the project directory

```bash
  cd icook/app
```

Install dependencies

```bash
  pip install -r /path/to/requirements.txt
```

Start the server

```bash
  python3 main.py
```

Go to the front-end app

```bash
  cd icook/icook-frontend
```

Install dependencies

```bash
  npm install tailwindcss uuidv
```

Start the server

```bash
  npm start
```



## API Reference

#### Retrieve a new recipe

```http
  POST /generate-recipe
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `ingredients` | `string` | Provides the data required to generate the recipe |


## Authors

- [@lucacodorean](https://www.github.com/lucacodorean)

