#Computing a set of restults for each tree distance measure and every size 'k'
#These results are:
#  maximum / minimum distance between two examples
#  average time taken and average distance between all examples,

import json

def compute_results():
    k_array = [4,5,6,7,8,9,10,11,12,16,20,24,32,40,48,64,128,192,256]
    ar_cted = {"time": [], "cost": [], "max": [], "min": []}
    ar_cted_a = {"time": [], "cost": [], "max": [], "min": []}
    ar_ated = {"time": [], "cost": [], "max": [], "min": []}
    ar_ated_a = {"time": [], "cost": [], "max": [], "min": []}
    ar_sted = {"time": [], "cost": [], "max": [], "min": []}
    ar_sted_a = {"time": [], "cost": [], "max": [], "min": []}
    ar_grf1 = {"time": [], "cost": [], "max": [], "min": []}
    ar_grf64 = {"time": [], "cost": [], "max": [], "min": []}
    for k in k_array:
        cted = cted_a = ated = ated_a = sted = sted_a = grf1 = grf64 = {'time': 0, 'cost': 0, 'count': 0,
        'max': 0, 'min': 9999999}
        file_name = 'examples/example_trees_size_' + k.__str__() + '.json'
        if os.path.exists(file_name):
            with open(file_name) as tree_file:
                tree_list = json.load(tree_file)
            for tree in tree_list:
                if 'GRF1' in tree and tree['GRF1'].get('time') and tree['GRF1'].get('cost') :
                    grf1 = {
                        'time': grf1.get('time') + tree['GRF1'].get('time'),
                        'cost': grf1.get('cost') + tree['GRF1'].get('cost') / k,
                        'count': grf1.get('count') + 1,
                        'max': max(grf1.get('max'), tree['GRF1'].get('cost')),
                        'min': min(grf1.get('min'), tree['GRF1'].get('cost'))
                        }

                if 'GRF64' in tree and tree['GRF64'].get('time') and tree['GRF64'].get('cost'):
                    grf64 = {
                        'time': grf64.get('time') + tree['GRF64'].get('time'),
                        'cost': grf64.get('cost') + tree['GRF64'].get('cost') / k,
                        'count': grf64.get('count') + 1,
                        'max': max(grf64.get('max'), tree['GRF64'].get('cost')),
                        'min': min(grf64.get('min'), tree['GRF64'].get('cost'))
                        }

                if 'CTED' in tree and tree['CTED'].get('time') and tree['CTED'].get('cost'):
                    cted = {
                        'time': cted.get('time') + tree['CTED'].get('time'),
                        'cost': cted.get('cost') + tree['CTED'].get('cost') / k,
                        'count': cted.get('count') + 1,
                        'max': max(cted.get('max'), tree['CTED'].get('cost')),
                        'min': min(cted.get('min'), tree['CTED'].get('cost'))
                        }

                if 'CTED_a' in tree and tree['CTED_a'].get('time') and tree['CTED_a'].get('cost'):
                    cted_a = {
                        'time': cted_a.get('time') + tree['CTED_a'].get('time'),
                        'cost': cted_a.get('cost') + tree['CTED_a'].get('cost') / k,
                        'count': cted_a.get('count') + 1,
                        'max': max(cted_a.get('max'), tree['CTED_a'].get('cost')),
                        'min': min(cted_a.get('min'), tree['CTED_a'].get('cost'))
                        }

                if 'ATED' in tree and tree['ATED'].get('time') and tree['ATED'].get('cost'):
                    ated = {
                        'time': ated.get('time') + tree['ATED'].get('time'),
                        'cost': ated.get('cost') + tree['ATED'].get('cost') / k,
                        'count': ated.get('count') + 1,
                        'max': max(ated.get('max'), tree['ATED'].get('cost')),
                        'min': min(ated.get('min'), tree['ATED'].get('cost'))
                        }

                if 'ATED_a' in tree and tree['ATED_a'].get('time')  and tree['ATED_a'].get('cost'):
                    ated_a = {
                        'time': ated_a.get('time') + tree['ATED_a'].get('time'),
                        'cost': ated_a.get('cost') + tree['ATED_a'].get('cost') / k,
                        'count': ated_a.get('count') + 1,
                        'max': max(ated_a.get('max'), tree['ATED_a'].get('cost')),
                        'min': min(ated_a.get('min'), tree['ATED_a'].get('cost'))
                        }

                if 'STED' in tree and tree['STED'].get('time') and tree['STED'].get('cost'):
                    sted = {
                        'time': sted.get('time') + tree['STED'].get('time'),
                        'cost': sted.get('cost') + tree['STED'].get('cost') / k,
                        'count': sted.get('count') + 1,
                        'max': max(sted.get('max'), tree['STED'].get('cost')),
                        'min': min(sted.get('min'), tree['STED'].get('cost'))
                        }

                if 'STED_a' in tree and tree['STED_a'].get('time') and tree['STED_a'].get('cost'):
                    sted_a =  {
                        'time': sted_a.get('time') + tree['STED_a'].get('time'),
                        'cost': sted_a.get('cost') + tree['STED_a'].get('cost') / k,
                        'count': sted_a.get('count') + 1,
                        'max': max(sted_a.get('max'), tree['STED_a'].get('cost')),
                        'min': min(sted_a.get('min'), tree['STED_a'].get('cost'))
                        }
            if cted.get('count'):
                ar_cted["time"].append(cted.get('time') / cted.get('count'))
                ar_cted["cost"].append(cted.get('cost') / cted.get('count'))
                ar_cted["max"].append(cted.get('max'))
                ar_cted["min"].append(cted.get('min'))
            if cted_a.get('count'):
                ar_cted_a["time"].append(cted_a.get('time') / cted_a.get('count'))
                ar_cted_a["cost"].append(cted_a.get('cost') / cted_a.get('count'))
                ar_cted_a["max"].append(cted_a.get('max'))
                ar_cted_a["min"].append(cted_a.get('min'))
            if ated.get('count'):
                ar_ated["time"].append(ated.get('time') / ated.get('count'))
                ar_ated["cost"].append(ated.get('cost') / ated.get('count'))
                ar_ated["max"].append(ated.get('max'))
                ar_ated["min"].append(ated.get('min'))
            if ated_a.get('count'):
                ar_ated_a["time"].append(ated_a.get('time') / ated_a.get('count'))
                ar_ated_a["cost"].append(ated_a.get('cost') / ated_a.get('count'))
                ar_ated_a["max"].append(ated_a.get('max'))
                ar_ated_a["min"].append(ated_a.get('min'))
            if sted.get('count'):
                ar_sted["time"].append(sted.get('time') / sted.get('count'))
                ar_sted["cost"].append(sted.get('cost') / sted.get('count'))
                ar_sted["max"].append(sted.get('max'))
                ar_sted["min"].append(sted.get('min'))
            if sted_a.get('count'):
                ar_sted_a["time"].append(sted_a.get('time') / sted_a.get('count'))
                ar_sted_a["cost"].append(sted_a.get('cost') / sted_a.get('count'))
                ar_sted_a["max"].append(sted_a.get('max'))
                ar_sted_a["min"].append(sted_a.get('min'))
            if grf1.get('count') > 5:
                ar_grf1["time"].append(grf1.get('time') / grf1.get('count'))
                ar_grf1["cost"].append(grf1.get('cost') / grf1.get('count'))
                ar_grf1["max"].append(grf1.get('max'))
                ar_grf1["min"].append(grf1.get('min'))
            if grf64.get('count') > 5:
                ar_grf64["time"].append(grf64.get('time') / grf64.get('count'))
                ar_grf64["cost"].append(grf64.get('cost') / grf64.get('count'))
                ar_grf64["max"].append(grf64.get('max'))
                ar_grf64["min"].append(grf64.get('min'))

    differences = {
        'CTED': [],
        'CTED_5': [],
        'STED': [],
        }
    for i in range(0, len(k_array)):
        differences['CTED'].append(ar_cted['cost'][i] - ar_cted_a['cost'][i])
        differences['CTED_5'].append(ar_ated['cost'][i] - ar_ated_a['cost'][i])
        differences['STED'].append(ar_sted['cost'][i] - ar_sted_a['cost'][i])


    result_data = {
        'GRF1': ar_grf1,
        'GRF64': ar_grf64,
        'CTED': ar_cted,
        'CTED_a': ar_cted_a,
        'CTED_5': ar_ated,
        'CTED_5_a': ar_ated_a,
        'STED': ar_sted,
        'STED_a': ar_sted_a,
        'Differences adapted': differences
        }
    with open('results/result_data.json', 'w') as outfile:
        json.dump(result_data, outfile)

if __name__ == "__main__":
    for tree_size in [4,5,6,7,8,9,10,11,12,16]:
        number_of_trees = 100
        #compare_trees(tree_size, number_of_trees)
        create_graph(tree_size, number_of_trees, "low_grf_high_ted")
    #compute_results()
    #create_time_graph()

