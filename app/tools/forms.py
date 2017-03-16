from flask_wtf import Form
from wtforms import SubmitField, StringField, SelectField, FileField, IntegerField
from wtforms.validators import Required

class DbBlastForm(Form):
    pass

class BlastForm(Form):
    myChoices = range(1,6)
    filename = FileField('Test File') #,validators=[Required()])
    outfmt = StringField('Outfmt.', default='6')
    block_size = StringField('Size of blocks to split file into.', default='100k')
    blastAlgorithm = StringField('blastn or blastp', validators=[Required()])
    evalue = StringField('Evalue')
    submit = SubmitField('Submit job.')
    # TODO implement Blast form

class AddForm(Form):
    x = IntegerField('x')
    y = IntegerField('y')

class BlastNForm(Form):
    pass

class RaxmlForm(Form):
    pass
