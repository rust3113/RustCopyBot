import telegram.error
from moviepy.editor import *
from telegram import Update, InputMediaVideo
from telegram.ext import CallbackContext
import moviepy.editor as moviepy
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Отправьте мне видео, я преобразую его в видеокружок.\n"
                                    "Важно: проверьте в настройках вашего аккаунта во вкладке Конфиденциальность разрешение на отправку вам голосовых и видеосообщений!\n"
                                    "И, что бы ваше видео длилось менее минуты!")








async def process_video(update: Update, context: CallbackContext):
    try:
        video_file = await context.bot.getFile(update.message.video.file_id)
        await video_file.download_to_drive("input_video.mp4")

        # Prеобразование видео в видеокружок


        input_video = VideoFileClip("input_video.mp4")
        w, h = input_video.size
        circle_size = 360
        aspect_ratio = float(w) / float(h)

        if w > h:
            new_w = int(circle_size * aspect_ratio)
            new_h = circle_size
        else:
            new_w = circle_size
            new_h = int(circle_size / aspect_ratio)


        resized_video = input_video.resize((new_w, new_h))

        output_video = resized_video.crop(x_center=resized_video.w/2, y_center=resized_video.h/2, width=circle_size, height=circle_size)
        output_video.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac", bitrate="1.4M")


        with open("output_video.mp4", "rb") as video:
            await context.bot.send_video_note(chat_id=update.message.chat_id, video_note=video, duration=int(output_video.duration), length=circle_size)
            return 'input_video.mp4'
    except telegram.error.BadRequest:
        await context.bot.send_message(chat_id=update.message.chat_id, text="Видео слишком большое! Оно должно быть менее 1 минуты!")
        return