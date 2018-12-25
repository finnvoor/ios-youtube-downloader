import appex
import clipboard
import youtube_dl
import console
import sys
import glob
import os
import dialogs


class Format:
	''' Format class represents available audio/video formats '''
	
	def __init__(self, id, description, ext):
		self.id = id
		self.description = ext + ' - ' + description.split('- ', 1)[1]
		self.ext = ext
	

def download(video_url):
	available_formats = []
	with youtube_dl.YoutubeDL({}) as ydl:
		meta = ydl.extract_info(video_url, download=False)
	formats = meta.get('formats', [meta])
	
	descriptions = ['Best']
	for format in formats:
		f = Format(format['format_id'], format['format'], format['ext'])
		available_formats.append(f)
		descriptions.append(f.description)
	selected_format = dialogs.list_dialog(
		title='Select a Format',
		items=descriptions
	)
	if selected_format is None:
		return
	format_to_use = 'best'
	ext = 'mp4'
	for format in available_formats:
		if selected_format == format.description:
			format_to_use = format.id
			ext = format.ext
	with youtube_dl.YoutubeDL({
		'format': format_to_use
	}) as ydl:
		ydl.download([video_url])
	
	list_of_files = glob.glob('*.*')
	latest_file = max(list_of_files, key=os.path.getctime)
	console.open_in(latest_file)
	if ext in latest_file:
		os.remove(latest_file)
	
	
def main():
	if not appex.is_running_extension():
		if len(sys.argv) == 2:
			url = sys.argv[1]
		else:
			url = clipboard.get()
	else:
		url = appex.get_url() or appex.get_text()
	if url:
		download(url)
		console.hud_alert('Done.')
	else:
		console.hud_alert('No input URL found.')

if __name__ == '__main__':
	main()
