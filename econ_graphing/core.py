from copy import deepcopy

import plotly.graph_objs as go
import yaml

plot1_data = {
    'lines': {},
    'intersections': [],
    'arrows': [],
    'annotations': [],
    'areas': [],
    'config_override': {}
}

config_defaults = {
    'x_label_offset': 5,
    'y_label_offset': 5,
    'min_x': 0,
    'max_x': 110,
    'min_y': 0,
    'max_y': 110,
    'x_title': 'Quantity of widgets',
    'y_title': 'Price of widgets',
    'max_x_offset': 5,
    'line_color': 'Black',
    'intersection_width': 1,
    'intersection_style': 'dash',
    'fillcolor': 'rgba(128, 0, 128, 0.7)',
    'text_color': 'Black',
}


def create_line_coefficients(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0] * p2[1] - p2[0] * p1[1])
    return A, B, -C


def compute_intersection(L1, L2):
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y
    else:
        return False


def add_lines(lines, layout, conf):
    if lines is None:
        return {}, layout, None
    lcoeffs = {}
    label_data = []
    for ln in lines:
        extreme1 = lines[ln]['left_point'][0] + (
            100 - lines[ln]['left_point'][1]) / lines[ln]['el']
        extreme2 = lines[ln]['left_point'][0] - (
            lines[ln]['left_point'][1]) / lines[ln]['el']
        max_x = min(max(extreme1, extreme2), 90) - conf['max_x_offset']
        y_val = lines[ln]['left_point'][1] + (
            max_x - lines[ln]['left_point'][0]) * lines[ln]['el']
        lcoeffs[ln] = create_line_coefficients(lines[ln]['left_point'],
                                               [max_x, y_val])
        layout['shapes'].append({
            'type': 'line',
            'x0': lines[ln]['left_point'][0],
            'y0': lines[ln]['left_point'][1],
            'x1': max_x,
            'y1': y_val,
            'line': {
                'color': lines[ln].get('color', conf['line_color']),
                'width': 3,
            },
        })
        label_data.append((max_x + conf['x_label_offset'],
                           y_val + conf['y_label_offset'], lines[ln].get(
                               'label', ln)))

    x, y, text = list(zip(*label_data))
    line_data = go.Scatter(
        x=x,
        y=y,
        text=text,
        mode='text',
    )

    return lcoeffs, layout, line_data


def add_intersections(intersections, lcoeffs, layout, conf):
    if intersections is None:
        return layout, {}
    intersection_values = {}
    for intersection in intersections:
        intinfo = intersections[intersection]
        inter_point = compute_intersection(lcoeffs[intinfo['line1']],
                                           lcoeffs[intinfo['line2']])
        if inter_point:
            layout['shapes'].append({
                'type': 'line',
                'x0': inter_point[0],
                'y0': 0,
                'x1': inter_point[0],
                'y1': inter_point[1],
                'line': {
                    'color': intinfo.get('color', conf['line_color']),
                    'width': 1,
                    'dash': 'dash',
                },
            })
            if intinfo.get('x-axis-label'):
                layout['xaxis']['ticktext'].append(intinfo['x-axis-label'])
                layout['xaxis']['tickvals'].append(inter_point[0])
                intersection_values[intinfo['x-axis-label']] = inter_point[0]

            layout['shapes'].append({
                'type': 'line',
                'x0': 0,
                'y0': inter_point[1],
                'x1': inter_point[0],
                'y1': inter_point[1],
                'line': {
                    'color': intinfo.get('color', conf['line_color']),
                    'width': intinfo.get('width', conf['intersection_width']),
                    'dash': intinfo.get('line-style',
                                        conf['intersection_style']),
                },
            })
            layout['yaxis']['tickvals'].append(inter_point[1])
            layout['yaxis']['ticktext'].append(intinfo['y-axis-label'])
            intersection_values[intinfo['y-axis-label']] = inter_point[1]

    return layout, intersection_values


def shade_areas(shading, intersection_values, layout, lines, conf):
    if shading is None:
        return layout
    for shade in shading:
        shade_data = {}
        if shading[shade]['type'] in ['rect', 'rectangle']:
            shade_data['type'] = 'rect'
            for k in ['x0', 'x1', 'y0', 'y1']:
                try:
                    shade_data[k] = float(shading[shade][k])
                except ValueError:
                    shade_data[k] = intersection_values[shading[shade][k]]
                except TypeError:
                    line_point_dict = shading[shade][k]
                    if line_point_dict['type'] == 'line-value-at':
                        x_value = intersection_values[line_point_dict[
                            'x-value']]
                        y_value = get_line_value_at(line_point_dict['line'],
                                                    lines, x_value)
                        shade_data[k] = y_value
            shade_data['fillcolor'] = shading[shade].get(
                'color', conf['fillcolor'])
            shade_data['line'] = {'width': 0}
            shade_data['layer'] = 'below'
            layout['shapes'].append(shade_data)
    return layout


def get_line_value_at(ln, lines, x_value):
    y_value = (lines[ln]['left_point'][1] +
               (x_value - lines[ln]['left_point'][0]) * lines[ln]['el'])
    return y_value


def add_annotations(annotations, intersection_values, lines, conf):
    if annotations is None:
        return None
    adata_dict_template = {
        'x': [],
        'y': [],
        'mode': 'text',
        'name': 'not needed',
        'text': [],
        'textposition': 'bottom'
    }
    annotation_data = []
    for a in annotations:
        adata_dict = deepcopy(adata_dict_template)
        adata_dict['text'].append(a)

        adata_dict['textfont'] = {
            'color': annotations[a].get('color', conf['line_color'])
        }
        for k in ['x', 'y']:
            value = annotations[a]['{}-value'.format(k)]
            offset = annotations[a]['{}-offset'.format(k)]
            try:
                adata_dict[k].append(float(value) + offset)
            except ValueError:
                adata_dict[k].append(intersection_values[value] + offset)
            except TypeError:
                if k != 'y':
                    raise RuntimeError('line value is only valid for y-value')
                if value['type'] == 'line-value-at':
                    x_value = intersection_values[value['x-value']]
                    y_value = get_line_value_at(value['line'], lines, x_value)
                    adata_dict[k].append(y_value + offset)
        annotation_data.append(go.Scatter(**adata_dict))
    return annotation_data


def econ_plot(yamldata):
    data = yaml.load(yamldata)
    conf = deepcopy(config_defaults)
    conf.update(data.get('configuration', {}))

    layout = {
        'title': data.get('title', ''),
        'xaxis': {
            'range': [conf['min_x'], conf['max_x']],
            'showgrid': True,
            'title': conf['x_title'],
            'tickvals': [],
            'ticktext': []
        },
        'yaxis': {
            'range': [conf['min_y'], conf['max_y']],
            'showgrid': True,
            'title': conf['y_title'],
            'tickvals': [],
            'ticktext': []
        },
        'shapes': [],
        'showlegend': False,
    }

    lcoeffs, layout, line_data = add_lines(data.get('lines'), layout, conf)
    layout, intersection_values = add_intersections(
        data.get('intersections'), lcoeffs, layout, conf)
    layout = shade_areas(
        data.get('shading'), intersection_values, layout, data.get('lines'),
        conf)
    annotation_data = add_annotations(
        data.get('annotations'), intersection_values, data.get('lines'), conf)

    fig = {'layout': layout, 'data': []}
    if line_data is not None:
        fig['data'].append(line_data)
    if annotation_data is not None:
        fig['data'] += annotation_data

    return fig
