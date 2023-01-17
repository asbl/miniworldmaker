import miniworldmaker.tokens.token as token_mod
import miniworldmaker.tokens.token_plugins.text_token.text_token as text_token
import miniworldmaker.tokens.token_plugins.widgets.widget_costume as widget_costume


class WidgetText(text_token.Text):
    pass


class WidgetImage(token_mod.Token):
    def get_costume_class(self):
        return widget_costume.WidgetPartCostume
