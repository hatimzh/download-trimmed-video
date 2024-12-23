import os
import subprocess
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'videos/index.html', {})

@csrf_exempt
def trim_video(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        # Vérifiez si le dossier de sortie existe, sinon créez-le
        output_dir = 'output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Chemin de sortie pour la vidéo téléchargée
        output_path = os.path.join(output_dir, "downloaded_video.mp4")

        # Commande pour télécharger la vidéo de 00:00:00 à end_time avec yt-dlp
        download_command = [
            'yt-dlp',
            '--merge-output-format', 'mp4',  # Assurez-vous que le fichier fusionné est mp4
            '--download-sections', f"*00:00:00-{end_time}",
            '-o', output_path,
            video_url
        ]

        # Exécution de la commande de téléchargement avec la durée spécifiée
        subprocess.run(download_command)

        # Chemin de sortie pour la vidéo découpée
        trimmed_output_path = os.path.join(output_dir, "trimmed_video.mp4")

        # Commande pour couper la vidéo avec ffmpeg si start_time est défini
        if start_time:
            trim_command = [
                'ffmpeg',
                '-i', output_path,
                '-ss', start_time,           # Start time for trimming
                '-c', 'copy',                # Copy codec (no re-encoding)
                trimmed_output_path
            ]

            # Exécution de la commande de découpe
            subprocess.run(trim_command)

            # Renvoie l'URL de la vidéo découpée
            return JsonResponse({'status': 'success', 'video_url': f"{request.scheme}://{request.get_host()}/output/trimmed_video.mp4"})

        # Renvoie l'URL de la vidéo téléchargée
        return JsonResponse({'status': 'success', 'video_url': output_path})

    return JsonResponse({'status': 'error'}, status=400)
