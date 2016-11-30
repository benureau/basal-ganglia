import prepare


def compute_changes(params):
    changes = {'task': {'single': {}, 'choice': {}}}
    changes['task']['single']['n_trials'] = params['n_trials']

    cue_freq_a = params['cue_freq_a']
    changes['task']['single']['cue'] = [cue_freq_a, 1.0 - cue_freq_a, 0, 0]

    rwd_freq_a = params['rwd_freq_a']
    for name in ['single', 'choice']:
        changes['task'][name]['rwd'] = [rwd_freq_a, 1.0 - rwd_freq_a, 0.0, 0.0]

    return changes

session = prepare.session # default


if __name__ == '__main__':
    prepare.copy_json('.')
    for idx, params in enumerate(prepare.param_generator()):
        changes = compute_changes(params)
        prepare.write_changes(idx, changes)
