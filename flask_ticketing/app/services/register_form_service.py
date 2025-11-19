from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import EmailField, SubmitField
from wtforms.validators import data_required, length
from wtforms.validators import EqualTo


class RegisterForm(FlaskForm):
    username = StringField(
        "Username", 
        validators=[
            data_required(), 
            length(min=3, max=20)
            ]
        )
    
    email = EmailField(
        "Email", 
        validators=[data_required()]
    )
    
    password = PasswordField(
        "Password", 
        validators=[
            data_required(),
                length(min=6)
            ]
    )
    
    confirm = PasswordField(
        "Confirm", 
        validators=[data_required(),
                    EqualTo("password", "Passwords must match")
                    ]
    )
    
    submit = SubmitField("Register")