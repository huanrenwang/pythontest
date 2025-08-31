import yaml

# 读取yaml内容
yaml_content = yaml.load("""
name: Vorlin Laruknuzum
sex: Male
class: Priest
title: Acolyte
hp: [32, 71]
sp: [1, 13]
gold: 423
inventory:
- a Holy Book of Prayers (Words of Wisdom)
- an Azure Potion of Cure Light Wounds
- a Silver Wand of Wonder
""", Loader=yaml.FullLoader)

yaml_content['name'] = 'New Name'
new_yaml = yaml.dump(yaml_content)
print(new_yaml)
print(new_yaml)

