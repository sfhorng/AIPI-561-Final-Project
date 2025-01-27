## Chatbot RAG App for American Movies
![Test, build, and push workflow status](https://github.com/sfhorng/AIPI-561-Final-Project/actions/workflows/main.yml/badge.svg?branch=main)

AIPI 561

[Demo video](https://duke.box.com/s/ffesfyffv021zrpd95ekl35hhvu49nn1)

## Purpose
The Streamlit application serves as a chatbot that focuses on providing information about <ins>select</ins> American movies across all decades starting from the 1900s. It retrieves output from a [Llamafile](https://github.com/Mozilla-Ocho/llamafile), TinyLlama, so it can be run locally from your personal machine. This Small Language Model is enriched with [scraped movie details](https://github.com/prust/wikipedia-movie-data)  from the wikipedia-movie-data repo that has been loaded into a local information vector_store file. The information includes release year, genre, main cast and crew, and plot summary. The application uses the [LlamaIndex framework](https://docs.llamaindex.ai/en/stable/) to connect to the Llamafile, retrieve the relevant context for the query, and retrieve the final output from the Llamafile.

## Architecture Diagram
For some background, the following are the steps used to create the vector store, or index. This is a one-time step that has already been completed, so you would be able to use this output in step 3 of the "Setting up" section below. The vector store will be loaded into memory upon app startup.

![Index creation sequence](https://github.com/user-attachments/assets/2a570bd0-92e7-44d0-8348-e04191ed0d3f)

The following are the steps taken to retrieve the response for a given prompt after app startup.

![Main architecture diagram](https://github.com/user-attachments/assets/90e80a5c-5b30-42b8-be14-0bd798d901d6)

## Setting up
1. Clone the repository, cd into it, and unzip vector_store.zip.
2. Install [Docker](https://www.docker.com/products/docker-desktop/) if you haven't already.
3. Copy and paste the [command from packages](https://github.com/sfhorng/AIPI-561-Final-Project/pkgs/container/aipi-561-final-project) into a terminal to pull the Docker image from the GitHub container registry. If you would like to build the image locally instead, please run ```make build_local```.
4. Download the TinyLlama-1.1B file from https://github.com/Mozilla-Ocho/llamafile?tab=readme-ov-file#other-example-llamafiles. Please move the file into the repository folder.
5. Run ```chmod +x TinyLlama-1.1B-Chat-v1.0.F16.llamafile```

## Testing the app
The following are steps to test the app in your local environment, as there is a step in the workflow that will run the tests before building the image. Please note that this is not needed to run the app.
1. Create a virtual environment with ```python3 -m venv .venv```
2. Activate the virtual environment with ```source .venv/bin/activate```
3. Run ```make test``` to run the unit tests.

![Sample output for unit tests](https://github.com/user-attachments/assets/85fb5cb5-73b3-4516-9133-a97717a1e4b8)

## Running the app
1. Start the Llamafile by running ```make start_model```. If you encounter any issues, please refer to the README from step 3 in the "Setting up" section above for more information.
2. In another terminal window, run ```make start_container``` to start the application. If you built the image locally, please run ```make start_container_local```. It may take a minute to load.

![UI with sample question](https://github.com/user-attachments/assets/177ae17c-4427-4024-b309-4058ed573190)
3. Start interacting with the application by typing in your query. It may take a moment for the response to start appearing.

While interacting with the application, please keep in mind the following limitation: Depending on which movie is being asked about, there may be some inaccuracies. Details from selected movies will be used by the model to provide the final output. Please refer to ```titles_in_vector_store.json``` for the specific movie titles that are represented. Since the model is probability-based, be sure to fact-check the output. 

## Example conversations
<ins>Q&A about one movie</ins>

User: Hi. Can I get a paragraph summary of the movie Monsters, Inc.?

Expected answer: 

Monsters, Inc. is a 2001 American computer-animated comedy film produced by Pixar Animation Studios for Walt Disney Pictures. Featuring the voices of John Goodman, Billy Crystal, Steve Buscemi, James Coburn, Mary Gibbs, and Jennifer Tilly, the film was directed by Pete Docter from a screenplay by Andrew Stanton and Daniel Gerson. The film centers on two monsters, the hairy James P. "Sulley" Sullivan (Goodman) and his one-eyed partner and best friend Mike Wazowski (Crystal), who are employed at the titular energy-producing factory Monsters, Inc., which generates power by scaring human children. However, the monster world believes that the children are toxic, and when a little human girl Boo (Gibbs) sneaks into the factory, she must be returned home before it is too late.

<ins>Conversation about one movie</ins>

User: Hi. Who directed the movie Ratatouille?

Expected answer:

The movie Ratatouille was directed by Brad Bird.

---

User: What year was it released?

Expected answer:

The movie Ratatouille was released in 2007.

---
User: What genre is it?

Expected answer: 

Ratatouille is a comedy-drama film.

---

<ins>Asking about multiple movies</ins>

User: Who directed Full Metal Jacket?

Expected answer: 

The director of Full Metal Jacket is Stanley Kubrick.

---

User: What other movies did he direct? Please list three only.

Expected answer:

Sure, here are three other movies directed by Stanley Kubrick:

- Barry Lyndon (1975)
- A Clockwork Orange (1971)
- Paths of Glory (1957)

I hope that helps!

---

User: Thanks! What are a couple other movies that haven't been mentioned yet from Stanley Kubrick? Please list two only.

Expected answer:

Sure, here are two more movies directed by Stanley Kubrick:

- The Shining (1980)
- Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb (1964)

I hope that helps!

## Performance/Evaluation 

### Approach

<ins>Metric and Components Evaluated</ins>
- The metric used for evaluation is accuracy based on implementing RAG. 
- Since the Wikipedia movies dataset includes a few main components, plot summary, release year, genre, and main cast and crew, the evaluation will be on each of these component for a chosen movie. Since the number of cast and crew members listed can vary, for simplicitly, the director has been chosen to represent whether the cast and crew component is accurate.
- A sample of ten movies with information in the vector store will be evaluated alongside a sample of ten movies that do not have information in the vector store. Please refer to ```titles_in_vector_store.json``` for which titles are represented. Due to the number of titles, the evaluation cannot be comprehensive, so the goal is to provide a quick snapshot of whether implementing RAG tends to improves accuracy. The output from the model may vary for the plot summary, so the accuracy results will be based on the output from the evaluation.

<ins>Title Selection and Criteria for Evaluation</ins>
- To try to keep other variables that could influence accuracy constant, the movies were chosen arbitrarily but had to be ones that are relatively well-known so that 1) someone who watches American movies of all genre types regularly would likely be familiar with and so that 2) the model would likely have some information on them without an external data source. Whether a movie is "well-known" is also rather subjective, so this is a best estimate effort to evaluate whether the retrieval portion of the chatbot improves accuracy. 
- The list of movies chosen represents a wide variety of genres.
- The prompts used were the same across all the chosen movies to retrieve the outputs, substituting only the title name, which is the exact title that is provided in the vector store.
- If any portion of the plot summary is inaccurate, the plot summary component would be considered inaccurate.

### Results

<ins>Movies that are **not** represented in the vector store</ins>
| Title  | Plot summary | Release year | Genre | Director |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| Singin' in the Rain | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| The Conjuring | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| The Hangover | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Clueless | :x: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Ford v Ferrari | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Doctor Strange | :x: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Rush Hour 2 | :x: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Monsters University | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| A Walk to Remember | :x: | :white_check_mark: | :white_check_mark: | :x: |
| Back to the Future | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |

<ins>Movies that **are** represented in the vector store</ins>
| Title  | Plot summary | Release year | Genre | Director |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| Folklore: The Long Pond Studio Sessions | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Oculus | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Lady Bird | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Knives Out | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Memento | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| The Amazing Spider-Man | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Rush Hour | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Toy Story 2 | :x: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| The Princess Diaries | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| The Terminator | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |

### Summary and Discussion
The following summarizes the above tables and includes the fraction of titles that had accurate information for each component evaluated.

| Represented in vector store? | Plot summary | Release year | Genre | Director |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| No | 6/10 | 10/10 | 10/10 | 9/10 |
| Yes | 9/10| 10/10 | 10/10 | 10/10 |

Although the results only include a small set of movies and the results can vary depending on the titles chosen, this evaluation suggests that the RAG implementation increases the likelihood that information about a movie, especially its plot summary, will be accurate. 

As you may have guessed, it is less likely for the model to provide a completely accurate plot summary due to the amount of information available on a movie, while it is more likely for the other components to have accurate responses because there is only one correct answer (or only a handful of correct answers for the genre).
