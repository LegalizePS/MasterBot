from datetime import datetime
from time import time

import psutil
from telegram import Update
from telegram.ext import CallbackContext

from common import convert_to_GB, get_list_of_py, str_uptime
from const import KeyboardMK


class Stats:
    @staticmethod
    def command(update: Update, context: CallbackContext):
        stat_msg = f"""
<b>Server Stats</b>
        There are <b>{len(list(get_list_of_py()))}</b> python programs running in your server.
    
    <b>CPU Percent</b>: {psutil.cpu_percent(interval=0.1)}%
    <b>RAM</b>: {psutil.virtual_memory().percent}%
    <b>DISK</b>: {convert_to_GB(psutil.disk_usage('/').used)}GB of {convert_to_GB(psutil.disk_usage('/').total)}GB used
    <b>Uptime</b>: {str_uptime(time() - psutil.boot_time())}
    <b>Booted on</b>: {datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")}

    <b>Stats as of</b> {datetime.fromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S")}
"""
        if update.callback_query:
            try:
                update.callback_query.edit_message_text(
                    stat_msg, parse_mode="HTML", reply_markup=KeyboardMK.refresh_stats()
                )
            except:  # raises "BadRequest:Message not modified" if there's no change in stats
                pass
        else:
            update.effective_message.reply_text(
                stat_msg, parse_mode="HTML", reply_markup=KeyboardMK.refresh_stats()
            )

    @staticmethod
    def detail_command(update: Update, context: CallbackContext):
        to_send = """
<b>Detailed stats of <pre>py</pre> processes</b>
<pre> Alias   Threads   Memory Percent</pre>

    """
        for p in get_list_of_py():
            # Assume the last arg is Alias
            to_send += (
                "<pre>"
                + " ".join(
                    str(arg)
                    for arg in (p.cmdline()[-1], p.num_threads(), p.memory_percent())
                )
                + "</pre>\n"
            )
        update.effective_message.reply_html(to_send)
