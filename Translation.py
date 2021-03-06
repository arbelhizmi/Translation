!pip install --force-reinstall --extra-index-url=https://pip.repos.neuron.amazonaws.com "torch-neuron==1.7.*" "transformers==4.0.1" sentencepiece "neuron-cc[tensorflow]"
from transformers import MarianMTModel, MarianTokenizer
import json


__doc__ = """
Author: Arbel Hizmi
This Python file provides translation services.
Translation services are made by HelsinkiNLP group, using the transformers library
"""

class TranslationUtils:
  """
  This class provides translation services. Currently only English to Hebrew 
  and Hebrew to Russian translations are supported.
  """
  MODEL_NAME = 'Helsinki-NLP/opus-mt-{}-{}'
  SUPPORTED_LANGUAGES = {"English": "en",
                         "Hebrew": "he",
                         "Russian": "ru"}
  def __init__(self, debug=False):
    self.debug = debug

  def load_model_and_translate(self, source_language: str, destination_language: str, text_to_translate: str) -> json:
    """
    Function to load relvant model and translate given text. 
    The only possible translate options are: English to Hebrew, Hebrew to Russian.
    :param source_language: language to translate from. Option are: English, Hebrew (Capital matter)
    :param destination_language: desired language to translate to. Option are: Hebrew, Russian (Capital matter)
    :param text_to_translate: text to translate
    :return: JSON object with the following fields:
      'source_language': source language
      'destination_language': destination language
      'original_text': the original text
      'translated_text': will contain the translated text as string, and if failure occurred it will have value of None
      'succeeded': boolean which indicate if operation was successful or not
      'message': if operation succeded, this field can be ignored. If operation failed, this field will contain informative message

    Example for possible inputs: ('English', 'Hebrew', 'Today is Tuesday')
    """
    # Checks if source language is 'Hebrew' and destination language is 'Russian'
    # Or if source language is 'English' and destination language is 'Hebrew'
    if (source_language == 'Hebrew' and destination_language == 'Russian') or \
    (source_language == 'English' and destination_language == 'Hebrew'):
      
      model_name = MODEL_NAME.format(
          self.SUPPORTED_LANGUAGES[source_language],
          self.SUPPORTED_LANGUAGES[destination_language])
      
      # Load the relevant model and translate text
      tokenizer = MarianTokenizer.from_pretrained(model_name)
      model = MarianMTModel.from_pretrained(model_name)
      translate = model.generate(**tokenizer(text_to_translate, return_tensors="pt", padding=True))
      translated_text = [tokenizer.decode(t, skip_special_tokens=True) for t in translate]

      if self.debug:
        print(translated_text[0])

      data_to_export = {'source_language': source_language,
                        'destination_language': destination_language,
                        'original_text': text_to_translate,
                        'translated_text': translated_text[0],
                        'succeeded': True,
                        'message': "Text was translated successfully"
                        }

    # Any other input is illegal
    else:
      data_to_export = {'source_language': source_language,
                'destination_language': destination_language,
                'original_text': text_to_translate,
                'translated_text': None,
                'succeeded': False,
                'message': "Invalid inputs. Currently, possible language-pairs are: 'English' & 'Hebrew' or 'Hebrew' & 'Russian'"
                }
    
    data_as_json = self.dictionary_to_json(data_to_export)
    return data_as_json


  @staticmethod
  def dictionary_to_json(data_to_export: dict) -> json:
    """
    Function to convert data from dictionary to JSON
    :param data_to_export: data to convert to JSON
    :return: JSON object. If operation succeeded, value of succeeded will be True. If data_to_export cannot be
      converted to JSON, "succeeded" field will be False, and no translated text will be returened.
    """
    try:
      output_as_json = json.dumps(data_to_export, ensure_ascii=False, indent=4)
    
    except TypeError as error_message:
      output_as_json = output = {'source_language': source_language,
                                 'destination_language': destination_language,
                                 'original_text': text_to_translate,
                                 'tanslated_text': None,
                                 'succeeded': False,
                                 'message': error_message
                                 }

    return output_as_json


m = TranslationUtils(True)
hebrew = m.load_model_and_translate('English', 'Hebrew', 'Hello, I like to eat 5 apples every day')
hebrew = m.load_model_and_translate('English', 'Hebrew', "It's difficult to run a marathon")
hebrew = m.load_model_and_translate('English', 'Hebrew', 'Neural networks is a very interesting subject')


russian = m.load_model_and_translate('Hebrew', 'Russian', '????????, ?????? ???????? ????????????')
russian = m.load_model_and_translate('Hebrew', 'Russian', '???????? ???? ???????? ???????? ???????? ?????? ???????? ??????')
russian = m.load_model_and_translate('Hebrew', 'Russian', '???????????? ???? ???????????? ?????????? ????????????')

