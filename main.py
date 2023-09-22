import flet as ft
import threading
import time
from math import pi

import cv2
import base64
import time

import pandas as pd
import os

workouts = pd.DataFrame(
    {
        "Exercises": ['Overhead Press', 'Lateral Lift'],
        "Reps": [5, 3],
        "Daily": [1, 2],
        "Weekly": [1, 1]
        }
    )

class HomeView:
    numWorkoutsText = ft.Text()
    numWorkoutsText.size = 24

    numWorkoutsColumn = ft.Column()
    numWorkoutsColumn.alignment = 'center'
    numWorkoutsColumn.controls = [numWorkoutsText]

    numWorkoutsRow = ft.Row()
    numWorkoutsRow.alignment = 'center'
    numWorkoutsRow.controls = [numWorkoutsColumn]


    numWorkoutsCard = ft.Card()
    numWorkoutsCard.content = numWorkoutsRow

    numWorkoutsCompletedText = ft.Text()
    numWorkoutsCompletedText.size = 24

    numWorkoutsCompletedColumn = ft.Column()
    numWorkoutsCompletedColumn.alignment = 'center'
    numWorkoutsCompletedColumn.controls = [numWorkoutsCompletedText]

    numWorkoutsCompletedRow = ft.Row()
    numWorkoutsCompletedRow.alignment = 'center'
    numWorkoutsCompletedRow.controls = [numWorkoutsCompletedColumn]


    numWorkoutsCompletedCard = ft.Card()
    numWorkoutsCompletedCard.content = numWorkoutsCompletedRow


class WorkoutView:
    placeholder = ft.Image(src = 'assets/hep.jpg', width = 300, height = 300)
    b64_string = None         
    image_box = ft.Image(src_base64=b64_string, width=300, height=300, gapless_playback=True)
    video_container = ft.Container(image_box, alignment=ft.alignment.center, expand=True)
    video_container.content = placeholder

    current_rep_progress_bar = ft.ProgressBar()
    current_rep_progress_bar.expand = True
    current_rep_progress_bar.bar_height = 20
    current_rep_progress_bar.value = 0.0

    rep_text = ft.Text()
    rep_text.size = 35
    rep_text.value = '4 Reps'

    first_row = ft.Row()
    first_row.controls = [current_rep_progress_bar]
    
    second_row = ft.Row()
    second_row.controls = [video_container]
    
    third_row = ft.Row(spacing = 20)
    third_row.alignment = 'center'
    third_row.controls = [rep_text]
    #third_row.wrap = True

    column = ft.Column()
    column.alignment = 'center'
    column.controls = [first_row, second_row, third_row]

    container = ft.Container()
    container.content = column

    card = ft.Card()
    card.width = 700
    card.height = 450
    card.content = container
    

def main(page : ft.Page):
    page.title = "fletCam"

    def RepBar(height, width, percentage):
        remaining_percentage = 1-percentage 
        remaining_percentage_scaled = int(remaining_percentage * height)
        container = ft.Container()
        container.bgcolor = 'blue'
        container.width = width
        container.height = height
        repbar = ft.Container()
        repbar.bgcolor = 'grey'
        repbar.height = remaining_percentage_scaled
        column = ft.Column()
        column.controls = [repbar]
        container.content = column
        container.animate = 1
        return container

    def add_rep_bar(height, width, percentage):
        rep_goal = 4
        if 'reps' in page.session.get_keys():
            reps = page.session.get('reps')
        else:
            page.session.set('reps', 1)
            reps = 1
        workout_view.rep_text.value = f"{reps} / {rep_goal} reps"
        repbar = RepBar(height = height, width=width, percentage=percentage)
        workout_view.third_row.controls.append(repbar)
        page.session.set('reps', reps+1)
        page.appbar.actions = [ft.FilledButton("Form 80%")]
        page.update()

    def update_images():
        cap = cv2.VideoCapture(0)
        while(cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True and page.session.get('play_state') == True:
                if page.session.get('play_state') == False:
                    break
                # encode the resulting frame
                jpg_img = cv2.imencode('.jpg', frame)
                b64_string = base64.b64encode(jpg_img[1]).decode('utf-8')
                image_box.src_base64 = b64_string
                page.update()
            else:
                break
            time.sleep(1/115)

    def stop_playing(e):
        page.session.set('play_state', False)
        stop.on_click = start_playing
        stop.text = 'Start'
        stop.icon = ft.icons.FACE_UNLOCK_OUTLINED
        stop.width = 100
        page.update()

    def start_playing(e):
        page.session.set('play_state', True)
        workout_view.video_container.content = image_box
        stop.text = 'Stop'
        stop.on_click = stop_playing
        ## theading 
        update_image_thread = threading.Thread(target=update_images)
        update_image_thread.daemon = True
        update_image_thread.start()
        page.update()

    def page_switch(new_page):
        page.controls.clear()
        if new_page == 'home':
            home_view.numWorkoutsCompletedText.value = '10'
            home_view.numWorkoutsText.value = '20'
            page.add(home_view.numWorkoutsCard)
            page.add(home_view.numWorkoutsCompletedCard)
        if new_page == 'workouts':
            page.add(workout_view)



    appbar = ft.AppBar()
    appbar.title = ft.Text('Movision')
    appbar.leading = ft.Icon(ft.icons.ANALYTICS)
    page.appbar = appbar

    homeNav = ft.NavigationDestination()
    homeNav.icon = ft.icons.HOME
    homeNav.label = "Home"

    workoutNav = ft.NavigationDestination()
    workoutNav.icon = ft.icons.SPORTS
    workoutNav.label = "Dash"

    navigationBar = ft.NavigationBar(destinations= [homeNav, workoutNav])
    page.navigation_bar = navigationBar

    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
     
    b64_string = None         
    image_box = ft.Image(src_base64=b64_string, width=300, height=300, gapless_playback=True)

    stop = ft.FloatingActionButton(text = 'Start')
    stop.on_click = start_playing
    stop.icon = ft.icons.ANALYTICS
    stop.width = 100
    page.floating_action_button = stop

    placeholder = ft.Image(src = 'https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/a258b2108677535.5fc364926e4a7.gif', width = 300, height = 300)
    b64_string = None         
    image_box = ft.Image(src_base64=b64_string, width=300, height=300, gapless_playback=True)
    video_container = ft.Container(image_box, alignment=ft.alignment.center, expand=True)
    video_container.content = placeholder

    current_rep_progress_bar = ft.ProgressBar()
    current_rep_progress_bar.expand = True
    current_rep_progress_bar.bar_height = 20
    current_rep_progress_bar.value = 0.0

    rep_text = ft.Text()
    rep_text.size = 35
    rep_text.value = '4 Reps'

    first_row = ft.Row()
    first_row.controls = [current_rep_progress_bar]
    
    second_row = ft.Row()
    second_row.controls = [video_container]
    
    third_row = ft.Row(spacing = 20)
    third_row.alignment = 'center'
    third_row.controls = [rep_text]
    #third_row.wrap = True

    column = ft.Column()
    column.alignment = 'center'
    column.controls = [first_row, second_row, third_row]

    container = ft.Container()
    container.content = column

    card = ft.Card()
    card.width = 700
    card.height = 450
    card.content = container

    def on_shake(e):
        if 'shake_count' in page.session.get_keys():
            shakecount = page.session.get('shake_count')
            print(shakecount)
        else:
            page.session.set('shake_count', 1)
            shakecount = 1
            print(shakecount)
        shakecount = shakecount + 1
        page.session.set('shake_count', shakecount)
        


    workout_view = WorkoutView()
    home_view = HomeView()
    page.add(workout_view.card)
    page.add(ft.TextButton('press', on_click=lambda _: add_rep_bar(height=50, width=10, percentage=0.8)))

    page.update()


ft.app(target=main, port=port, view = ft.WEB_BROWSER)
