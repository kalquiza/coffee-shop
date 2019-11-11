# Coffee Shop

## Full Stack Coffee Shop

Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard. This coffee shop web application serves the digital menu experience with the following features:

1) Display graphics representing the ratios of ingredients in each drink.
2) Allow the public to view drink names and graphics.
3) Allow the shop baristas to view the recipe information.
4) Allow the shop managers to create new drinks and edit existing drinks.

## Getting Started


### Backend

The `./backend` directory contains the completed Flask server with a pre-written SQLAlchemy module to simplify your data needs. Instructions on installing backend dependencies and running the backend application are detailed in the `README.md` of the `./backend` directory. Additionally, API reference and testing instructions can also be found here.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. Instructions on installing frontend dependencies and running the frontend application are detailed in the `README.md` of the `./frontend` directory.

[View the README.md within ./frontend for more details.](./frontend/README.md)

### Running the Application

After setting up both the backend and frontend we can run the complete application altogether. To run the full application:

From the `./backend/src` directory run:


```bash
export FLASK_APP=api.py;

flask run --reload
```

From the `./frontend` directory run:

```bash
ionic serve
```

To see the full application in action, open the frontend application running at `http://localhost:8100/`

## Authors

Coffee Shop application implemented by Kristoffer Alquiza. Project starter code provided by the Full Stack Web Developer Course at [Udacity](https://www.udacity.com/course/).

## Acknowledgements
This project was completed as part of the Full Stack Web Developer Course at [Udacity](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044). Credit to the Udacity team for providing the couse content and starter code for this application.