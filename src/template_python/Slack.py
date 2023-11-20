# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from template_python.credentials import getpwd
from pathlib import Path
from . import log, ic
ic.configureOutput(prefix=f'{Path(__file__).name} -> ')

class Blocks:
    def __init__(self) -> None:
        self.DIVIDER = {"type": "divider"}
    
    def TEXT(self, text: str, img_url: str='', img_alt: str ='') -> dict:
        block = {
                    "type": "section",
                    "text": { "type": "mrkdwn", "text": text}
                }
        
        if img_url != '':
            block["accessory"] = {
                        "type": "image",
                        "image_url": img_url,
                        "alt_text": img_alt
                        }
        return block
        
    def IMAGE(self, img_url: str, alt_txt: str='', text: str='') -> dict:
        block: dict = {
                "type": "image",
                "image_url": img_url,
                "alt_text": alt_txt
                }
        
        if text != '':
            block['title'] = {
                "type": "plain_text",
                "text": text,
                "emoji": True
                }
        return block

    def HEADER(self, text: str) -> dict:
        return {
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": text,
				"emoji": True
			}
		}
        
class Slack:
    def __init__(self):
        self.client = WebClient(token=getpwd('Slack-pythonbot', 'token'))
        self.BLOCK = Blocks()
        return
    
    def __str__(self) -> str:
        return "SlackAPI Instance"
    
    def __repr__(self) -> str:
        return "Slack()"

    def channel_id(self, channel_name:str) -> str:
        """Returns channel id for the specified channel name
        """
        return getpwd('Slack-pythonbot', channel_name)

    def init_block(self):
        self.block = []
        return
    
    def msg(self, message:str, channel:str="python") -> int:
        """Sends Slack message
        """
        err = 0
        try:
            _ = self.client.chat_postMessage(
                channel=self.channel_id(channel),
                text=message)
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            print(f'NG - Slack message not sent: {str(e)}')
            err = 1
        return err
    
    def post_block(self, channel: str, blocks: list[dict]):
        """Posts the currently constructed block to slack chat
        Args:
            channel (str): Channel name
        """
        err = 0
        try:
            _ = self.client.chat_postMessage(channel=self.channel_id(channel),
                                                    blocks=blocks)
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            print(f'NG - Slack message not sent: {str(e)}')
            err = 1
        return err