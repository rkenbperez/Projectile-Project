import matplotlib
matplotlib.use('Agg')

from django.shortcuts import render
import math
import matplotlib.pyplot as plt
import io
import base64
from .forms import ProjectileForm

g = 9.8

def calculate_projectile(angle, vel, h1, h2=0):
    rad_angle = math.radians(angle)
    s = math.sin(rad_angle)
    c = math.cos(rad_angle)
    
    v0x = vel * c
    v0y = vel * s
    
    max_h = h1 + ((vel * vel) * (s ** 2)) / (2 * g)
    range_x = ((vel ** 2) * 2 * s * c) / g
    t_flight = 2 * (vel * s) / g
    
    results = {
        'v0x': round(v0x, 2),
        'v0y': round(v0y, 2),
        'vFx': round(v0x, 2),
        'vFy': round(-v0y, 2),
        'max_height': round(max_h, 2),
        'horizontal_range': round(range_x, 2),
        'time_of_flight': round(t_flight, 2),
        'time_to_max': round(t_flight / 2, 2),
    }
    return results

def calculate_derivatives(angle, vel, h1):
    """Calculate derivatives for motion analysis"""
    rad_angle = math.radians(angle)
    v0y = vel * math.sin(rad_angle)
    g = 9.8
    
    t_max_height = v0y / g if g != 0 else 0
    h_max = h1 + (v0y * t_max_height) - (0.5 * g * t_max_height**2)
    
    rate_of_change = []
    times = [0, t_max_height/2, t_max_height, t_max_height*1.5, t_max_height*2]
    
    for t in times:
        if t >= 0 and t <= t_max_height * 2:
            v_t = v0y - g * t
            rate_of_change.append({
                'time': round(t, 2),
                'velocity': round(v_t, 2),
                'acceleration': round(-g, 2)
            })
    
    return {
        'v0y': round(v0y, 2),
        't_max_height': round(t_max_height, 2),
        'h_max': round(h_max, 2),
        'rate_of_change': rate_of_change,
        'acceleration': round(-g, 2)
    }

def create_height_graph(vel, angle, h1, g=9.8):
    s = math.sin(math.radians(angle))
    t_flight = 2 * vel * s / g
    
    T = 0.0
    heights = []
    times = []
    
    while T <= t_flight + 0.1:
        h = s * vel * T - 0.5 * g * T ** 2 + h1
        heights.append(h)
        times.append(T)
        T += 0.02
    
    plt.figure(figsize=(10, 6))
    plt.plot(times, heights, 'b-', linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Height (m)')
    plt.title('Height vs Time')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return image_base64

def projectile_view(request):
    context = {}
    
    if request.method == 'POST':
        form = ProjectileForm(request.POST)
        if form.is_valid():
            angle = form.cleaned_data['angle']
            velocity = form.cleaned_data['velocity']
            h1 = form.cleaned_data['initial_height']
            
            results = calculate_projectile(angle, velocity, h1)
            derivatives = calculate_derivatives(angle, velocity, h1)
            graph = create_height_graph(velocity, angle, h1)
            
            context = {
                'form': form,
                'results': results,
                'derivatives': derivatives,
                'graph': graph,
                'angle': angle,
                'velocity': velocity,
                'h1': h1,
            }
        else:
            context = {
                'form': form,
                'error': 'Please check your input values'
            }
    else:
        form = ProjectileForm()
        context['form'] = form
    
    return render(request, 'visualizerApp/projectile.html', context)