from flask_wtf import Form
from wtforms import SubmitField, StringField, SelectField, FileField, IntegerField
from wtforms.validators import Required

class DbBlastForm(Form):
    pass

class BlastForm(Form):
    fasta = FileField('Fastafile') #,validators=[Required()])
    outfmt = StringField('Outfmt.', default='6')
    block_size = StringField('Size of blocks to split file into.', default='100k')
    blastAlgorithm = StringField('blastn or blastp', default='blastn', validators=[Required()])
    evalue = StringField('Evalue', default='1e-06')
    cloud_provider = SelectField('Cloud provider', choices=[('AWS','Amazon Web Services'), \
                                                            ('GCE', 'Google Cloud Engine'), \
                                                            ('Azure', 'Microsoft Azure')])
    submit = SubmitField('Submit job.')

class AddForm(Form):
    x = IntegerField('x')
    y = IntegerField('y')

class BlastNForm(Form):
    pass

class RaxmlForm(Form):
    pass
