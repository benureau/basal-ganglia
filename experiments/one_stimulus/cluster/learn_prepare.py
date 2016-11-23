import prepare


def compute_changes(params):
    changes = {'model': {'Hebbian': {}, 'RL': {}}}
    changes['model']['RL']['LTP'] = params['rl_ltp']
    changes['model']['RL']['LTD'] = 0.8*params['rl_ltp']
    changes['model']['Hebbian']['LTP'] = params['rl_ltp']/params['hebb_ratio']
    changes['model']['RL']['init'] = params['rl_init']

    return changes


if __name__ == '__main__':
    prepare.copy_json('.')
    for idx, params in enumerate(prepare.param_generator()):
        changes = compute_changes(params)
        prepare.write_changes(idx, changes)
