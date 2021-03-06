# -*- coding: utf-8 -*-
# Phatch - Photo Batch Processor
# Copyright (C) 2007-2008 www.stani.be
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/
#
# Phatch recommends SPE (http://pythonide.stani.be) for editing python.

# Follows PEP8

from core import models
from lib.reverse_translation import _t
from lib.imtools import has_transparency

OTHER_IMAGE = _t('Image')
FOLDER = _t('Folder')
FILL_TYPES = (OTHER_IMAGE, FOLDER)


def init():
    #lazily import
    global _tamogen
    import other.tamogen as _tamogen
    _tamogen.OTHER_IMAGE = OTHER_IMAGE
    _tamogen.FOLDER = FOLDER
    _tamogen.FILL_TYPES = FILL_TYPES


def mosaic(image, fill_type, fill_image, fill_folder, columns, rows,
        canvas_width, canvas_height):
    if has_transparency(image):
        image = image.convert('RGBA')
    else:
        image = image.convert('RGB')
    return _tamogen.mosaic(image, fill_type, columns, rows,
        canvas_width, canvas_height, fill_image, fill_folder)


class Action(models.Action):
    label = _t('Tamogen')
    author = 'Juho Vepsäläinen'
    email = 'bebraw@gmail.com'
    init = staticmethod(init)
    pil = staticmethod(mosaic)
    version = '0.1'
    tags = [_t('filter')]
    __doc__ = _t('Tone altering mosaic generator')

    def interface(self, fields):
        fields[_t('Fill Type')] = self.ChoiceField(
            FILL_TYPES[0], choices=FILL_TYPES)
        fields[_t('Fill Image')] = self.ReadFileField('<path>')
        fields[_t('Fill Folder')] = self.FolderField(
            '<folder>/<subfolder>', choices=self.FOLDERS)
        fields[_t('Rows')] = self.PositiveNonZeroIntegerField(10)
        fields[_t('Columns')] = self.PositiveNonZeroIntegerField(10)
        fields[_t('Canvas Width')] = self.PixelField('100%',
            choices=self.PIXELS)
        fields[_t('Canvas Height')] = self.PixelField('100%',
            choices=self.PIXELS)

    def values(self, info):
        #pixel fields
        width, height = info['size']
        # pass absolute reference for relative pixel values such as %
        return super(Action, self).values(info, pixel_fields={
            'Canvas Width': width,
            'Canvas Height': height})

    def get_relevant_field_labels(self):
        relevant = ['Fill Type', ]

        action = self.get_field_string('Fill Type')

        if action == OTHER_IMAGE:
            relevant.append('Fill Image')
        elif action == FOLDER:
            relevant.append('Fill Folder')

        relevant.extend(['Rows', 'Columns', 'Canvas Width',
            'Canvas Height', ])

        return relevant

    icon = \
'x\xda\x01\x98\x15g\xea\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x000\x00\
\x00\x000\x08\x02\x00\x00\x00\xd8`n\xd0\x00\x00\x00\x03sBIT\x08\x08\x08\xdb\
\xe1O\xe0\x00\x00\x15PIDATX\x85e\x98Y\x90\\\xe7u\xdfo\x7f\xdfw\x97\xde\xa7\
\xd7\xe9}V`0\x1b\x16\x82\x03\x80\x8bl\xd1,Q\xb4E\xd9\xa5\x92eS\xb6\xac*\xb9\
\\eW%\x95T\x94\x87\x94\x9fR~\xd1[$&\x11YQ\x14;^(\xd36I\x912I\x01\x04@\xec\
\x00\x81Y\x00\xcc\x00\x83\x19\xcc\xd2=k\xcf\xda\xfb]\xbe\xfd\xe6\xa1\x07\xa0\
\xac\xbc\xfe\xea\xdcs_\xce\xaf\xce\xff;\x1e\xf7\xbf\xfd\xa5C\xa9\xf7\xe4\x88\
\xb2V>\x7fg\x1a3~B\x89[\x8c\x1d\xe9\xebg\xfb{\xef,\xcc\x13!\xfe\xf8\xd4I\x93\
\xd2\xe4\xf0\xb0\xb2\xbd\xf5\xe1\xf44\xe6\xfc\xf7N\x9f4\tM<sLY\xdf\xfcpb\x92\
p\xfeZ\xbe`R\xda92\xac\x94\xb7>\x98\x9e&\x9c\xbf\xfe\xf5g%&\xe0\xf9\xe3Ji\
\xe3\xf2\xd5)\x871w\xc3\x879{\xa9\xd0\xbfP\xdb?\xbf2O\x858\x9d\xee\xc2\x9c}9\
\xd7\xbfX\xdf?\xbf\xfa\x98\t\x01\xff\xec\xd4Q\x1dA\xcd\xc6\xff\xeb\xc2M\x04\
\x00\x13\x12\xd8\xae\n\x81F\xc8\x1b\xd3w\x11\x00L\xcaX8\xa0A\x18\xc4\xf8\x8d\
\x9b7\xdb$\x18\xf0k\x08\x06\x1c\xe7\xbf_\xbc\x8c\x00dR\x04\x00\xd0 \x0c:\xf8\
\x8d\x1b\x07}2I\xbf\x8e\x10\xb4\x9c\xff\xf3\x8bK*\x00T\x88\xea\x1eC\x00\xb6\
\x18}g\xee.\x04\x80\xbb\xd2\x87T\x15\xc0\x16\xa3\xff4\x7f\xafM\xe0\xef\x1f\
\x1d\xe8\xcb\xa5n\xcd/\xdf^-\xcf\xefV\r\x15)\xd8\x1d\x89\xc5/o\xae\xdf\xdb\
\xdf-6\x1a\x06B\x1d\x01\xdf\xb1\xce\xd4\xc5bq\xa2\\^\xac\xd6t\x84\xfc~\xdf\
\xd1L\xe6\xe2\xe3\xc5\x89\xf5\xf5\xc5\xbd}\x03!\x1f\x00\xc7S\xa9\x0b\xc5\xe2\
\xc4fy\xb1R3\x10\x8aF}\xf9\xae\xf4\xe4\xcc\xc2\xad\xe5\xf5\xb9\xed}\xaf\x86\
\xeaU\xd6\xd7\x11\x9b\xdcY\x7f\\\xdb\xdb0\x1b\x1a\x80:B\xbd\xe1\xd8\xd4\xee\
\xfa\xe3\xda^\xd9lh\x00z\xee\x7f\xff{B\xba!Cs\x18_\xdc\xafuu\x84v\x8b-\xe1\
\xbaAUu\x04_m63\xfe@,\xd1!\xa4\x1b\xd25\x87\xf3\xe5Z-\x1f\n\xa9\xe1\x80p\xdd\
\xa0\xae;\x8c\x15+\x95\\G\x07t\xf0\xd3\x9ab\xb5\x96\x0b\x87\x92=A!e\xc8\xab;\
\x94/\xecT\xbab\xe1+\xd7\xb7\xa5\xeb\xfaT\x8d\x08\xbee6\x13\xbe\x00P<\xc2u}H\
\xa5\x82oY\xcd\xb87\x80\x14Eib\x92\xf0{\xfb{\x0b\xa3\xdd\xc4\xc5\xf4\\\xb1e2\
\x1a5\x8c\xd3\xa9\xb4\x99\xa4-\xca\xb6\x14\xde\xa2$\xee\xf3\x1e\xcb\xe7Og\
\xb3MB\x1ea\xab\x89q\xcc\xef;\xd6\xdb}\x06\x17\x9a\x84<X*\xb6k\x8e\x17\n\xa7\
\xb3\xa4EIY\xb1\x1b\x0eI\x04\xfd\x85\x81\x9e\x81\xfe\x82\xe2\xe0+\xd7\xb7m\
\xceB\xba1\x12\xcf\xd9QfsZ\xaaW\x1dN\xc3\x9a>\x12\xcf\xd9\x9c\xd9\x8c\x82\
\xbaC\x98\x94\xf9l\xe7\xcd\xe99\x85\t\x0f\x84MJ\xb9\x94\xc3\xd1\xd8\xc7\xa5"\
\x11B\x83\xa0A\x08\x93r0\xd9y~~\x1es\xaeA\xd8\xc0\x98K9\x98N_\x98y\xf8\x84\
\x10&\xe4Pg\xe7\xa7ss\x84s\r\xc0\xba\x8d\x99\x10\x9d\x85\xf4\xf8\xf8\x03\x85\
1\x05A\x8bQ!eo8v}\xa3D\xa5@\x00Z\x8cr){\xc2\xb1\x1b\x9b%&\x84\n \x1aD\x1d\
\x96\xcb\x14\xea\x7f!\x94y\xe7\xca4\x11\xe2K\x89\x9c\xc5X8\x9az\xd5\x85\xff\
\xb24O\x84\xf8\xd6sg,J\x95B\xdf+\xaa\xef\x9fg\xee\x11\xce\xbf\xfbW\xff\x89Y\
\x8er\xe6\xe5\xafl/^\xfc\xf9G\x98\x92W_\xfb\xaa\x89\xb1\xf2\xc2\xf3_-\x96>\
\xbe|\x1536\x1a\xec\xb5=Ta\xbd\x87\xa3\xdaO?\x9d\xa4\x9c\xf7\'{0g=\xc9>\xa1\
\x06?+\xcd2)\xce\xe4\xfa0g\x872\x87<F\xf8\xb3\x95Y*\x04\xfc\xf6\xd0\x11\r\
\x02/&?\x1c\x9fl\xdb\xa1\xbbH\x85\x10P\xf2\xe3\x99{\x10\x00\xe6\xcah8\xac!\
\xe8s\xf0\x8fn^\x83\x000!\xb3\x83\xbd\xba\xa6"f\xfe\xf4\'\x7f\xa3BH9\xf7R\
\xae\xab\xc8gY?\xfe\xf9\x87\x08B&\x84B\\\x15B\x17\xdbo]\xbd\x8c `B2[ \x00M\
\x86\xdf\x9b\x9b\x80\x1e \xa4\xf4\xa9\x9a\n\xa1I\xf1\xbbs\xe3\x00\x00!\x05\
\xfcZ_\xdfh"\xf1\xd9\xea\xda\xdd\x9d\x9d\xe5Z]GPS\xe0p4~\xb5\xbc~\xbf\xb2Wj6\
t\x08C\xc1\xc0hg\xea\xb3\xe2\xd2\xd4\xd6\xe6r\xb5b \x14\xeb\xcbw\x0f\x0e\xdc\
\xb9\xf1\xf9\xe7\x0f\x1e\xcd\xaf\xac\x19\x9af01\xd4\xddu\xe5\xfe\xcc\xf8r\
\xf1qy\xdb\xd04\x85\xc9\xa1T\xe6\xda\xd2\xc2\xf4\xe6F\xa9\xb2\xaf#\xc4\x1c\
\xd9\x13I\xdc\xdb^[\xac\xee\x94\xcd\xba\n\xa1\xa1\xaa\xbd\x1d\x89\xbb;\xab\
\x0b\xd5\x9dr\xab\xaeB\xe4\xb9\xf0\xfa\xb7\xa4\xeb\x064\rs^\xaa7\xb2\xc1\x00\
5\xa5pe@\xd50\xe7\xab\xadf\xc6\x1f\xe8H\xc5\x85t\x83\xba\x8e\x19+\xd5k\xd9`(\
\xf3\xdao\x08!\xc2\x01\xbf\x8d\xc9\xe2\xdaFW\xba\x93\xad\x94\x85\x94!\xaf\
\xd7\xa1tig\'\x1f\x8b\xed\xacW\x84+\x03\xba\x81\x19[\xabV\xd2\xe1\x8eR\xa9"]\
\xd7\x8b4*\xf8\xb6\xd5\x88{\x03*\x84\xc2u}\xaaF\x05\xdf2\xebq_\x10)\x8a\xd2\
\xa24j\x18\xcf\x15\nc)\xda\xa2t\xd2\xdc1)\x8b\xea\xc6\xa9L\xded\xd4dlSQZ\x94\
\xc4|\xbe3\xf9\xc2\x18!-J\xf6\x15\xa5iY\x89HG\xf7\xc9\xe3C\xc7F\x14\xcb\x9eX\
)7\x1d\'\x1e\x0c\x0c\r\x8e\x9et\xfa\x1d\xc79\xb7^\xb1\x08\x89\xfa\xfcc\x85n3\
_0\t)\x95*\x0e\xa3!\xcd;\x94\xc88\x8c\xda\x9cn4\xab\x0e\xa7!\xdd\x18\x8a\x17\
\x06b)\x9bQ\xd0$\x94K9\x92\x88\xff\xeb\xd2\x12\x16Bm[\xe6\xca\xc1H\xfc\x97\
\xabE"\x84\n@\x13\x13.\xe4h\xb2\xf3\xa3\xf9GDp\r\xc2z\xcbd\\d\x06\x0e\xdd\
\xfe\xf4\x92B\xa9\xa2\xa2\x86ms!\xfa\xbb\xbb.\xdf\x1e\x97\x8c\xe9\x08\xb5\
\x08\xe6B\x0e\xa6\xd2\xe7\x1e=\xa4\x9ck\x10\xda\x8c\nWvw\xc4?\xdfXbR\xa8\x00\
Z\x8c\x08){:\x12\xb76\x96\xa8\x10\x08@O\xf5?\xff{\x93\xb2\xfc\xe0\x80\xb2\
\xb3\xf3\xee\x83G\x98\x8b\x97\x0b\xdd\x16\xa3\x87\x06\x06\xe4\xce\xee?>zD\
\x84x\xb9o\xccbtx\xe0\xa8\xb3\xbb\xf9\xcf\xb3\xf7\x08\xe7\'\x9e\xf9M\x9b\x92\
/\x8f\x8c\x95\xca\xab\xbf\xb8\x7f\x8br\xfe\xfd\xff\xf0-\xd3v:^yY\x99\x7f\xfc\
\xf1\xc7\xe70\xa5\xbeu\xee0\xfa\xd2\xa1\x91\xc5\xbd\xadO\xe7\xeeS\xc1\xff\
\xf2\x0f\xbelb\xd2\xf9\xdc)\xa5\xb4\xfa\xc1\xf5[\x98\xb1\xdf=y\xdc\xc4\xa4\
\xf3\xb9\xb16!\x8c\xc1?\x1a\x19\xd4 \x08`\xf2\xc3\xcf\'\x10\x00L\n/R5\x00u\
\x82\x7f4q\xe0\x9dO\x0f\xaa\x00A\xe2\xfc\x8f\xf1k\xc8\x03\x98\x94\xc8\x1fV!\
\xb2\x1d\xfb\xaf\xaf\x9fE\x00r!\xf2=I]U}\xcd\xd6\x8f\xff\xf6g\x08A\xc6yk\xbb\
\xa9Bd\x12\xfc\xce\xd4u\x08\x80\x90\xa2\'\xd3\xa1!\x14\xb4\xec\x1f}t\xb6\xbd\
\x13C^\xa3M\xde\xf8\xe8,\x02\x90\t\x01\xbf~\xa8\xefhg\xf2biujkg\xa9V\xd7!\
\xd4!\x1aM&.\xb5\xbd\xab\xd7u\x08\r\xd5?\x92L_Y]\xba\xbf\xb3Y\xacUt\x84\x80/\
8\x90\xca\xddZ~4\xbb\xb9\xb2Z\xd9\xd5\x91\x9a\xce\xc7\x86\x0e\xf5_\xb931\xfe\
h\xfe\xf1\xfa\x86\xa1k\xe6\x9e\xd9\x97\xe8\x9c\\[\x9e\xdf\xdd\xdclTT\x84\xf2\
\xc9\xd0\xb1\xae\xfc\xc5\x87\xb3\x13\xc5\x95\xc5\xed\x1d]U\xfd\xbav\xbc\x90\
\xbf\xf0`v\xa2\xb8\xb2\xb4\xb3k\xa8\xc8s\xf9;\x7f(\\\x19\xd24\x87\xf3b\xbd\
\x91\x0b\x06\x85P\x84t\x83\x9a\x8a\xb9(5\x1a\xd9`\xc0\x85Q)e@\xd31\xe7+\x8dj\
&\x18n\x05\xe3\xc2\x95~\xdd \x8cm\xd4\xf6:C\x91\x91\x17z\x85\x14!\x9f\xdf!di\
\xb3\x9cO&\xa6.L\x0bW\xfaT\x9d\n^nT\x13\x81\xf0\xa9\x91\xa4\x90n\xd0k8\x94\
\x16w\xf7r\xb1\xa8\x06\xa1\x902\xe85\x1c\xca\x8a\xbb{\xb9h\x04)\x8a\xd2",\
\xe6\xf5\x8e\xe5\xb2\xa7(mQz\xb7\xbcg2\x1a\xf3\x1ag\xb2\x99\x93\xb4\xd3\xa4l\
\xa6*Z\x94D\xbc\xbe\xd3\xd9\xaegh\xce\xa4\xe4s\xcc-\x82;|\x81g\n\xfd\x16\xe9\
1\tV\x14\xa5i\xd9\xf1px\xe8\xf8\xe8I\xcb\xc6\x96=ua\xda\xa64l\xf8F3\x85\xc1\
\xce\x9cM\x89\xa2\xc8\x16vbA\xff\x89\xc3C\xa71n9\xf8\xd1f\xb9\xe9\xe0X0p\xfc\
p\xffi\xa7\xa7\x851h\x12\xc2\xa5\x1cM&>YX\xc2\\\xa8\x00\xb6\xc9p"\xfe\xd1\
\xd22\x11B\x85\xa0E0\x97r8\x91\xfad\xf1\x11\x11\\\x85\xd0$\x8e\x90\xe2pg\xee\
\xe2\xa3{\x84s\x15\xa2\x86ir.\xfa\x0f\xf5]\xbetMR\xaa\xa9\xc8\xa4XH\xd1\x1bK\
]_\x9e\xa3\x82#\x08\x1b\x8e\xc3\x84\x1c\xce\xe7?\x9d\xbcK\x18\xd3\x10l\xd8\
\x0e\x97b(\x9f;?q\x97p\xae!\x84\xce\xe4\x0b\x16e0\x9b\xff\x1a\xd4\xdey8K\xb8\
8\x1a\xec\xb59\x0b\xa0\xae\xb1\xa8\xf1\xde\x83GTr({\x89\xa0\xf7\x14\xc32S?\
\x98\xbf\xc7]\xfeW\x7f\xf2\x8aE\xc8\xc0H\xd7\xe1\x88\xe7\x9d\x89\xdb\x84\xf3\
W\xf5a\x93r\xa5h\xbe\xe8\x86\xdf\xfe\xdf\xffB9;\xda\xd1\xe9p:\x12\x8c\xea\
\xe9\xeeO\x17\x1e2\xc9\xff\xcb\xf7^51Q\x8e\x1e\xfajP{\xff\xea-\xc2\xf8\xd7O\
\x1ek\x93W\x02\x07\x04~{x\xe8`\x97\xdd\x1eoO>\x10\x9a\n\x01!\xe4\xa7\x0f\' \
\xf00)M\xa2"\x00mN\xce\xafO\x00\x8fG\xb8r\xa0+\xae!\xa89\xf6\x1b\x97\xce#\
\x08\x98\x10\x01M\xd7 R\x1d\xfb\x8d+\xe7\xdb\xdeQ"T\x08M\x82\xdf\x99\xb9\x8d\
\x00\xe0R\xf6\x14\xe2\x1aB!\xcb\xfe\xe1\x87g\x11\x84\\\x88\x80\xd7\xf85\x02_\
;\xd4?\x9aL^ZY\x9d\xda\xde^\xae\xd5\r\x04=R\x1d\x88$om\xad>\xd8\xdfYm\xd5t\
\x80,\xaaf\x03\x89\xb9\xda\xeajkg\xd7\xa9\xab\x00\xf6f;F\xd2\xb9\xcb\x0bs\
\xf7\xd6W\x8b{\xbb\xba\xaa\xfaTm8\x93\xbd\xb28\x7foc\xb5\xb8\xbf\xab#\x95Q\
\xd1\x17MN\x96K\x8f\xf7\xb77\x9a5\r\xc2\\\xb6\xe3XW\xfe\xc2\xcc\xec\xe4\xf2\
\xca\xe2\xf6\xae\xae"\xbf\xae\xfd\x1a\xf1\\\xfc\xe3\xd7\x85\xeb\x065\xcdy\
\xb2\xcb\xaau \\\xe9G\x1a\x11|\xbd\xd5H\xf9\x833;\x1e\xe9J\x03jL\xf2}\xdc\
\x88\xe8\xc1W\xbeT\x10\xf2`O\xadT\xf7\xb3\xe1\x08T<\xc2\x95A\xdd\xc0\x8c\xae\
T+\x99pGic\xff\x8b|\xd8\xac\'\xfc\xc1g\x9f\xeb\x92O\x9d\xda\xd9\xcb\xc5"\x08\
B!e\xe8W\xc9\xc1.\xf3z\x9f\xcbe[\x94\xb6(\xbdR\xdf\xb7\x18\xed\xd0\xbd\xcftf\
\x8f2j1:\xb3\xb3O\x04\r\xa8\xde\xbep\x86\x08\x869U\x14\xa5Ep\xd4\x1f8\xd3\
\xd3\xd7"\xd8\xc4d\xae\xbci\x12\x1c\xf5\xf9Ow\x1f9Ip\x8b\x90\xd2\xc6\xbe\xcd\
hH\xf7\x8et\xe6\xec\x04\xb5\x19Q\x14\xa5\xe9\xe0X \xf0\xcc\xe8\xa1\xd3\xfdN\
\xd3\xc1\xb3\x1b\xe5\x96\x83\xe3\xc1\xc03\x03\x07\xe4`\x97\x8d&\x13\xbfXX$\\\
h\x00\xb6(\xe1R\x0eD\x12\x17W\x17\xa9\x10*\x80\x0e\'\xc2\x95Y\x7f\xfc\xfe\
\xfe\x12\x93\x1c\x02\xd0t\x1c.\xe4p:\xfb\xf1\x83\xfb\x94s\r\xc1&~B\x1eN\x13\
\xce5\x08-J\x84\x94\xbd\xd1\xc4\xf5\x95\x05*8\x02\xb0i;\\\x88\x91\xae\xdc\
\xb9\xf1)\xcc\xb8\x86\xd0\x01)|A\xd0H"k3\xa6G2/\x15\xd0\xbbs\xb3D\x08\xdd{F\
\x08b\xa2c\xd1\x8e\xdc\xdf-Nq\xc9\xc7\xba\xd2D\xb0\xe7\xb2\xa9T\x1d\\[\x9fcB\
\xfc\xc7\xc4I\x93\xd2@\x87\xef\x9b\xdd\xb9\xb3\xf7nc\xce\x07\xa3\xbd\x96\xa4\
a\xac\xbe\xe0O}p\xfd\x16\x11\xe2\x9b\xbfq\xc2"\xf4\xc4\xb1c\xc77S\xefMM\x11\
\xce\xff\xdd\xeb\xbf\xa7XXy\xfe\xc5W\x9f\xcf^\xf9\xe02\xa6\xeck\xdf~^\xb1\
\xb1r\xe6\xc5W_\xc8]\xf9\xe0\x12&\x0c~\xf3\xc8\x90\n\xa1B\xf0\x9b\x93\xe3\
\x07N\xb1\x10\x02\xc8b\xce\xbf.\\\x86\x00\nW\xf8\x90@\x00Z\x94\xfcbq\x12z\
\x80p\xc5h"\xa8#d`\xe7\xad\x1b\xd7U\x00\x98\x10L\xaa\x1a\x84\x8c\xe0\x9f\xdc\
\xbb\t\x01\xe0R\x86"~\rA\xc5q\xde\xbcr\xa5\x9d3\x0f\xf5\'4M\x05\xd4\xfc\xeb\
\x9f\xbc\xaf"H\x19O\xfa\xbd\xba\x8a\x00\xb3\xfe\xe6\'\xef#\x04\x19\x17\xf0\
\x95\xde\xbe\xe1D\xe2\xea\xda\xea\xf4\xeeN\xa9^\xd3!\xb2\x99\xbf\x10N?\xd8](\
\xd67v\xcc}\x04\x91\x01eW81\xb3\xbbV\xac\xefn\x9bu\x15\xa2\x81\xa8\xffpg\xea\
\xc6\xf2\xf2\x9d\xad\xcd\xc7\xd5\x8a\x81\x10w\xd1\x91X\xe7\xcd\x8d\xe2\x83\
\xdd\xad\xd5FUG(\x10\xf2\x0e\xa53\xd7\x16\x17\xa776J\x95\x8a\xae\xa2LW4w\xa4\
{\xea\xe6\xfd[\x0f\x97\xe6V\xca^]\xf3\xfb\x8c\xec`\xcf\xd4\x8d\xfb\xb7\x1e,\
\xce\xadl\x19\xba\xea\xf9\xf0[\xaf\x0by\x90\x18W\x9b\xf5L 8\xb3\x1b\x93\xae4\
T\x83\t\xb6kU\xa2\xde\x0e\xd5S\x95\xael\'\xbd]\xab\x11\xf5\x06\xbfq\xf8\xe0\
\xa5f3\xbeT\xab\x15B\xa1RS\n\xd7\r\xa8\x1a\x16|\xbdYK\xf9C\xfeL@\xb82\xa0\
\xeb\x98\xf1\xd5j%\x13\x0e\x8f\xbc\xd4#\x84\x0c\x07\xbc6\xa6\x0b\xeb;]\xa9\
\x98\xa6"!d(\xe0u0]X\xdf\xeeJ\xc5\x91\xa2(&\xa3\x11\xaf1\x96)\x9c\xa0)\x93\
\xd2\x99]\xe9p\x12\xd0\xfc\x03\x89n\'\x92w8\xd9jV1\xa3A\xcd;\x10\xcd8\x11\
\x8a9U\x14\xde\xa4$\xee\xf3\x1e\xcew\x1d\xa7\x84\x13Rj\x96-J"\x86\xf7d:o\xd2\
\xac\xc5\xc8\x9ab\x99\x84D|\xfe\xb1\xee\xee\x138o\x12\xa2(J\xc3r\x12\x91`\
\xee\xe4\xe0a\xd3Q,\xe7\xf1\xd2z\xc3\xb2\xdb\xe4\x90yX\xb1\x9c\x83]6\x14O\
\x9c]^\xa2Bh\x10\xda\x1c\x0bW\x16\xc2\xe9\x89\xad\x87Lr\x04\xa0\xc3\x88p\xdd\
B(>\xbe\xb5\xc4\xa4\x80\x00\xd61aBv\'S\xd7\xe6\x1f)\x9c#\x08[\x94pW\x0e\xc4:\
\xcf\x17\xe7\xa9\xe0*\x80M\x8c\xb9\x90\x83\xe9\xd4\xd9\x87\x0f\t\xe7*\x84\
\xf5\x96\xcd\xb8H\x0etO\x9c\xbf\xadP\xa6\xa8\xa8\xde\xb2\x18\x17\x89#\xdd\
\x93\xe7?o\x13\xf4\xec\xc0\x11\x9b\xd2\xce\xa1\xe1\xafF"\xef\xcfL\x13\xc1\
\xa3\xda!"\xa8\x0fD\x0b\x81\x9ek+\xd3\\\xf2\xe3\xf1\x02\x11,\x08\x0b=A\xe3\
\xfa\xea,\x97\xe2\xbf\x9e\xee\xb7\x18U<\xc1g#\xb9\xff;5C\x84x\xe9\xe5/\xdb\
\x94\xf4\x1e\x7f&\xba\x91}wr\x9cr\xfe\xf2\xa1>\x8b\xd2tw\xcfo\xab\xda{SS\x94\
\xf3\xeft?ky\x88B\xf4\xb1d\xfe\xbd\x7f\xb8\x80\x19\x7f\xed\xe4\xa8\xe9\x12\
\xc5\xd6\x9eM\xe4\xde\xfd\xbb\xf3\x84q\xf8\x8d\xd1\xa3*\x84\x12;o\xdd\xba\
\x01!`BVZ\x1a\xf2@\x9b\xe3K\xab7\xa1\x07\x08Wz!\x80\x00\xda\x1c_\\\x1d\x07\
\x1e \\1\x10\xd1T\x08!!\xff\xf3\xfe8\x04\x80K\xe1\x8bET\x88\\\xc7y\xf3\xb3\
\x0b\xed\x9d\xe8\xd7\x90\x06\xa1\xeb8o]\xbd\xd2N\x9e\x89\xb8_C0`:?\xfa\xb0\
\xbd\x01e\xd0\xd0\x0f2\xe4\x87\x17 \x00\\H\xf8\x95\xc3\x03\x83\x9d\xa9\xeb\
\xc5\xe2\xccV\xb9T\xab\xea\x10\xd5M5\x13\xec\\\xa8\x16\xd7[\xe5=\xa7\xaa\x02\
d@O6\x98x\\]]k\xed\xec\xd9u\x15\xa0\x9e\x906\x1cK\\\xddX\xbd\xbf\xb7]l\xd6u\
\x08\x8d\x8e\xf0P&{\xed\xf1\xfc\xcc\xfaZi\x7f_G\xc8\x8b\xe0`&s\xfd\xa9e\x08E\
"\xde\xa3]\xb9\x8b3s\x93\xcbk\x8b[{\x86\xaa\xfat\xedhw\xee\xe2\xf4\xfc\xe4\
\xf2\xda\xd2\xf6\x9e\xa1\xa9\x9e\xf7\xbe\xfb=\xe9\xba~M\xc3\x9c\xaf\xd5j\xe9\
P\xe8\xc6\x9cG\xbaRG:\x13\xbc\xea\xd4\xc2FH\xf7\x10\xe9\xba\x06\xd4\xa8\xe4\
\x15\xa7\xdea\x04\xbf\x92\x87\xf2W\xdcL\x07\x82JWFH\x190\x0c\xcc\xd8Ze?\xdd\
\xd1\x01%\x17R\x06\x0c\x1d3\xb6V\xad\xa6\xc3\xe1\xce\xbc_J7\xe8\xd5\x1d\xca\
\x8a;\xfb\xb9X\x04\x01\xf041\x96\xdaDQ\x14\x93\x90\x88\xd7;\x96/\x98\x19bRzc\
n\x87\x08\xeaW}=\xd1<\x11Y\xccI\xc5Z\xc3\x9c\xfaUc\xa0\xa3@x\n\x0b\xaa(\xd5\
\x16\xa3\x11\xc3{*\x975i\xdad\xf4\xa1\xa2X\x04G\xfd\xfe\xb1\x9e^\x13w\x99\
\x04?\xdeX5\t\x89\xf8}\xcfvu[\x84\x98\x84T\x94F\xd3\xc1\xb1\xa0\xff\xd9\x81\
\xbeS\xfd\xb8\xe5\xe0\xd9\xf5\xad\x96Cb\xc1\xc0\xd8\x91\xbeS\x0en9\x18\xb4\
\x08\xe1R\x1eIv\x9e\x9b\x9f#B\xa8\x10:\x9c\x08)\xd3\x81\xce\x07{\xf3\xbcm\
\x19\'\xd2\x95\x99@bfo\x89K\x81<\xb0E)\x97r(\x16\xffei\x91\x08\xae\x02\xd0\
\xc2\x0e\x97r0\x93=\xfb`\x9ar\xaeA\xd4\xc2\x98K1\x98J\x9f\x9b=\xb0\xacic.\
\xc4h!\xfb\xcb\xf1\xfb\x84q\r\xa1F\x9bte>\xb9s@\xd0\xa9\xc1\x01\x9b\x92\xdc\
\xc8\xe0oGC\xefO\xdd%\x9cG\xb9N\x05\xf7[2\xe7\x86\'\x8b\x93\xdc\x15\xbf\xd3\
\xdb\x8f\x05\x1b\xeb\x88&\xa0\xb8\xb95\xcf\xa4\xf8\xfe\xef\x8c\xb4(\x0b\r\
\xf5\xfca\xda\xfb\xcb\x99\x87X\xf0\xef\xfe\xc5\x1f)\x0eV~\xeb\xc5\xef,\x1c\
\xba~\xee\x92\xc3\xd8\x99\xde\xbcMh\xb6\'\xfbu\xcd\xf3\xee\xd4=*\xf8\x11\x10\
\xf50\x89A3S\xf1\xbey\xeb"\x15\xe2\xf9l\xb7\xc2\x85\xe3ie*\xc6\x9b7/R\xc9\
\xe17\x8e\x9fP!\x92\x8e\xf3\xd6\xd5+\xed9/\x97\x19\x04\x00\x0bzko\x1ax<R\x91\
q\xbf\x81<\xd0\xe6\xe4\x93\xd5\xbb\xc0\x03\x84+\x8f\xa5\xfc\xed\x9c\xf9\xe6\
\xad\xdb*\x04T\xc8|w\xd6P\x91\xd22\xff\xf6\x1f\x7f\x8e d\\P\x8b\xaa\x08\xba\
\x0e~\xf3\xca\xb5\xf6\x8b\xcf\x83%\x02\xb0E\xc9\xdb\x0f\xa6\xa0\x07p)}\xa8}\
\xfd o?\x9c\x82\xc0\xc3\xa5\x04[\xcdF2\x14\xbc\xba\xb8\xb0Y\xab\x8f\x97J\xfb\
\x96\xd9bf\x10\xf9\x8a\xad\xf5\x06m\xadY\xdb\x16w\xaa\xd8\xec\xd0\xfd\x0f*k\
\xfb\xb8\xf5\xb8^nRg\xad\xd9\x8c\x04\x02\xd7\x8a\xc5\x95F\xf3\xd2\xea\xfa\
\x8ee\xad\xec\xee+\xb1\xc8\xfd\xf1{\xcb\xdb\xbb\x17\xa6g\xb7j\x8d\xadF\xa33\
\x18\xbc\xba\xb0\xb8Y\xab\xdd.\x95\xf6Ms\xd72\xe3>\xdf\x9d\xcd\xd5m\xb3yog\
\xb3\x86\xed]\xdb\x8cy\xfdw\xcak\xdbV\xeb\xfeN\xb9\x86\x1d\xcf\xbb\x7f\xfe\
\xe7\xd2u\xfd\xbaN\x18[\xabVS\xe1\xf0\xd9\xcf\xb6\xa5"u\xa01\xc9\xeb\xb4\x15\
R\xfd]Q]\xba\xd2@\x1a\x13|\xd7iF\x8d\xc0\xef\x8f\xf8\x85\xeb\xb6_sK\xb5z!\
\x14\x8c\x9d\x19\xe5R\x86}>\x9b\x90\x85\xf2Nw26?\xb7&\\7\xa0\x7faYe\xbd!]\
\xd9\xce\x90\xe5V3\xe9\x0b\x00\x8fG\xba\xae\x0f\xa9D\x88\xb2\xd9H\xf8\x02HQ\
\x14\x13\x93\x88\xcf7\xd6\xd5e\x12b\x12rV\xd9\xa6\x82\xf9\xa0\x91\x0bd\xa9dD\
2E1\x1d\xc1\x02\xaaq8\x9a\xef\x15\x14s\xa6(N\x93\xd0\xb8\xd7{$\x9f;\x91\xa1\
\x94\x925Ei\xd8N2\x14J\x8f\x0e\xf6\xd9\xb6b;\xf3sk&!Q\x9fo\xac\xbb\xcb$\xc4\
\xc4\xe4\xfaz\xc3b,\xac{\x8f&\xd3v\x9cY\x8c\x16k\x15\x8b\xd1\x90n\x8c&36\xeb\
\xb49\x05-L\xb8\x14GR\xe9s\xb3\xb3m\x17\x88\xa0\xd2\x95I#\xfa\xb8\xb9\xc2]\
\x01=\xc0\xe6DJ\x99\x0f\xc4\'\xf7\x8aL\n\x08\xdaWG\xd1\x9bL\\\x9d_P\x04\xd7 \
\xacY6\xe3"\xda\xd7u\xf7\xda\xe7\ne\nB-L\xb8\x90G\xd2\xa9\xb3\x0fg\xdb\xa9\
\xb2\x9d!\xfb"\xb1\xabk\xcb\xed,jQ*\xa4\xec\x8f\xc4\xaf\xad-\xb7\xaf\x8e(Gu\
\x87\x83h\xc5\x1d\xf1D>\xb8t\x87J\xfe\xa7\xcf\xf58\x9c\xbd\xdc\xdd\xfb\xb8\
\x12<W\x9c\xa3B\xbc\x98k\x93\xecpU;\xbb<\xc7\x84\xe8\x05=\\2\x9b\x84C\xbe\
\xdc\x0f\xee\xccQ)^\xcc\xf7:\x8c\xd9\xcd9O\xc5\xfc\xc1\'\x7f\xcf\x84x>\xd7\
\xedp\xd6\xb1\x07\x86=\xb1w?\x9b\xa0\x82\xbf\x90\xed\xb19\x1b\x89\xa75\x80\
\xda}^\xc8\xf5\xd8\x9c\x8d&\xd2:< \xf0\x95\xde#*\x84-J~\xf6p\xaa\x9d\xf4\xbc\
H\xfd\x82\xb4/\x81\x9a\xda\xb6\xe3g\xb3S\x07\x17xUko\xf8\xb7\x1fNA\xf0\xe4Z\
\x08\xc0\xaf\x18$\xda\xf7\xc3\x83\x9a\xb6S\xaa\xaa\x02hR\xf2\xf6\xec\xc1\xbf\
|\xda\xaf\x13\xf8\xa5|o\x7f$>\xb1\xb5>\xbf\xbf\xbb\xd1\xaak\x10\x19\x08\xf5G\
\x12\x13[k\xf3\x95\xdd\x8dVC\x83\xc8\x8bP\x7f$\xfe\x05\x01\xc8P\xd5C\x91\xf8\
\xf8\xc1W\r\r"\x03\xa9\xfd\xd1\xf8xy}\xbe\xb2\xbb\xd1\xac\x1f\x90v\xe7\xa7\
\x04\x1e\xf4y\\\xd9]?\xf8\xea\xd7\x89\xe7\xadW\xbf)\\\xb7\xfd\nk\xcf9\xf4\
\x00\xe9\xba>U%\xfc\xc9\xe4\x03\xd0\xb6\x83\n\xbe\xd9j&}\x01\x04\x81\x94\xae\
O=\xb0#\xe9\x0b@\xd0\xfe\xaa]\xf3o\x08\xe1\xbc]\x03\x9ev~b\xd9\x93\x9a/\x08R\
\x14\xc5f4\xac\x1b\xa3\xc9|{\xce\x8b\xb5\xea\xc1\xe4\xa7\x0f&\xbfT\xaf\xdaO\
\xec\x18\x8a3\x8b\xd1\x95F\xd5\xe64l\x18G\x93\x19\x9buZ\x8c\x96\x1a\xd5v\x9f\
\xa3\xc9\xfcP<e3Z\xac\x1f\x18t4\x9d\xb7x\xa7\xcdX\xb1VyR\x93\xb6\xe2\xccf\
\xed\xce\xff\x86\x00\x93R!e\xdf\xaf\xcc\xb9u@b\xd7\xd6\x9f\x10\xf6\xd4\x8e\
\xe2S;\xf8S_\xa4P\xe1\xc1M\xbe/\x12\xbf\xba\xb6L\x05G\x00<5\xe8\xea\xda2\x13\
B\x05\xc0b\xe4\xc9W\xc5\xf6\xdd\xfe\xff\'\xff\x0f\x0eg\xf1L\xe0\x1bu\x1b\x00\
\x00\x00\x00IEND\xaeB`\x82\x1cp\xf1\xf2'
