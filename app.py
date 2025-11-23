from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, SubmitField, validators
import os
import main_functions
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


# function to get api key
def get_key(filename,api_name):
    api_key_dict = main_functions.read_from_file(filename)
    my_api_key = api_key_dict[api_name]
    return my_api_key


dog_api_key = get_key("api_key.json","dog_key")


# function to save api data to a json
def save_breeds(dog_api_key):
    url = "https://api.thedogapi.com/v1/breeds"
    headers = {"x-api-key": dog_api_key}
    breed_dict = requests.get(url, headers=headers).json()
    main_functions.save_to_file(breed_dict,"breeds.json")

# save json to local computer
# save_breeds(dog_api_key)


# load all breeds - for dropdown section in form
def get_breeds():
    return main_functions.read_from_file("breeds.json")


# get breed information - for dropdown section in form
def get_breed_info(breed_name):
    for breed in get_breeds():
        if breed["name"].lower() == breed_name.lower():

            # combine imperial and metric formats into one line
            weight_combined = f'{breed["weight"]["imperial"]} lbs / {breed["weight"]["metric"]} kg'
            height_combined = f'{breed["height"]["imperial"]} in / {breed["height"]["metric"]} cm'

            return {
                "name": breed["name"],
                "weight": weight_combined,
                "height": height_combined,
                "lifespan": breed.get("life_span", "Unknown"),
                "origin": breed.get("origin", "Unknown"),
                "bred_for": breed.get("bred_for", "Unknown"),
                "temperament": breed.get("temperament", "Unknown"),
                "image": breed.get("image", {}).get("url")
            }
    return "Breed not found."


# function to get random dog image - for radio button section in form
def get_random_image():
    url = "https://api.thedogapi.com/v1/images/search?limit=1"
    headers = {"x-api-key": dog_api_key}
    data = requests.get(url, headers=headers).json()
    if not data:
        return None
    return data[0]["url"]


# creating the form
class UserForm(FlaskForm):
    # dropdown for user to choose dog breed #1
    breed_dropdown1 = SelectField("Select a dog breed to see its information",
                                 [validators.DataRequired()], choices=[])

    # dropdown for user to choose dog breed #2
    breed_dropdown2 = SelectField("Select a dog breed to compare its information",
                                  [validators.DataRequired()], choices=[])

    # text input for user to enter fav dog breed
    breed_input = StringField("Enter your favorite dog breed", [validators.DataRequired()])

    # radio button (y/n) for random dog image
    random_pic = RadioField("Do you want to see a random dog picture?",
                            choices=[("Yes", "Yes"), ("No", "No")], default="No")

    # submit
    submit = SubmitField("Submit")


@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()

    # populate dropdown based on breeds in json
    breeds = get_breeds()
    form.breed_dropdown1.choices = [(item["name"], item["name"]) for item in breeds]
    form.breed_dropdown2.choices = [(item["name"], item["name"]) for item in breeds]

    if request.method == "POST":
        breed_dropdown1_entered = form.breed_dropdown1.data
        breed_dropdown2_entered = form.breed_dropdown2.data
        breed_input_entered = form.breed_input.data
        random_pic_entered = form.random_pic.data

        # breed information - dropdowns form section
        breed1_info = get_breed_info(breed_dropdown1_entered)
        breed2_info = get_breed_info(breed_dropdown2_entered)

        # breed information - text input section
        fav_breed_info = breed_input_entered

        # random image - radio button form section
        random_image = get_random_image() if random_pic_entered == "Yes" else None

        return render_template("form_results.html", breed1_info=breed1_info, breed2_info=breed2_info,
                               fav_breed_info=fav_breed_info, random_image=random_image)

    return render_template('form.html', form=form)

if __name__ == '__main__':
    app.run()