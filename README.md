# Chatbot for American Movies
AIPI 561

## Purpose
The Streamlit application serves as a chatbot that focuses on providing information about <ins>select</ins> American movies across all decades starting from the 1900s. It retrieves output from a [Llamafile](https://github.com/Mozilla-Ocho/llamafile), TinyLlama, so it can be run locally from your personal machine. This Small Language Model is enriched with [scraped movie details from Wikipedia](https://github.com/prust/wikipedia-movie-data) from the local information vector_store file, including release year, genre, main cast and crew, and plot summary. 

## Setting up
1. Install [Docker](https://www.docker.com/products/docker-desktop/) if you haven't already.
2. Copy and paste the [command from packages](https://github.com/sfhorng/AIPI-561-Final-Project/pkgs/container/aipi-561-final-project) to pull the Docker image from the GitHub container registry. 
3. Clone the repository, cd into it, and unzip vector_store.zip.
4. Download the TinyLlama-1.1B file from https://github.com/Mozilla-Ocho/llamafile?tab=readme-ov-file#other-example-llamafiles. Please move the file into the repository folder.
5. Run ```chmod +x TinyLlama-1.1B-Chat-v1.0.F16.llamafile```

## Running the app
1. Start the Llamafile by running ```make start_model```. If you encounter any issues, please refer to the README from step 3 in the section above for more information.
2. In another terminal window, run ```make start_container``` to start the application. It may take a minute to load.
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
