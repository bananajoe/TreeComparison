#Additional functions creating graphs with the previously computed data

import os
import json

def create_ted_to_grf1_graph(tree_size, number_of_trees):
    file_name = 'examples/example_trees_size_' + tree_size.__str__() + '.json'
    plot_name = 'plots/' + graph_type + '_trees_size_' + tree_size.__str__() + ".png"
    if os.path.exists(file_name):
        data = [[[] for _ in range(6)] for _ in range(number_of_trees)]
        with open(file_name) as tree_file:
            tree_list = json.load(tree_file)
        for i in range(0, len(tree_list)):
            j = 0
            for k in [1,64]:
                key = 'GRF' + str(k)
                if (key in tree_list[i]):
                    data[i][j] = tree_list[i][key]
                j = j + 1
            if ('ZSS' in tree_list[i]):
                data[i][3] = tree_list[i]['CTED']
            if ('STED' in tree_list[i]):
                data[i][4] = tree_list[i]['ATED']
            if ('STED_adapted' in tree_list[i]):
                data[i][5] = tree_list[i]['STED']
        sted_adapted_to_grf1 = [-1 for _ in range(number_of_trees)]
        sted_to_grf1 = [-1 for _ in range(number_of_trees)]
        grf64_to_grf1 = [-1 for _ in range(number_of_trees)]
        for i in range(0, len(data)):
            if (len(data) >= 5):
                if (data[i][4] and data[i][0] and data[i][2]) and data[i][5]:
                    sted_adapted_to_grf1[i] = float(data[i][5]) / float(data[i][0])
                    sted_to_grf1[i] = float(data[i][4]) / float(data[i][0])
                    grf64_to_grf1[i] = float(data[i][1]) / float(data[i][0])
        sorted_sted_to_grf1 = sorted(sted_to_grf1)
        sorted_grf64_to_grf1 = [x for _,x in sorted(zip(sorted_sted_to_grf1,grf64_to_grf1))]
        sorted_sted_adapted_to_grf1 = sorted(sted_adapted_to_grf1)
        if len(sorted_sted_to_grf1) > 0 :
            index = len(sorted_sted_to_grf1) - 1
            maximum = max(np.amax(sorted_sted_to_grf1), np.amax(sorted_grf64_to_grf1), np.amax(sorted_sted_adapted_to_grf1))
            plt.ylim(0, max(2.5, 0.2 + maximum))
            plt.plot(sorted_sted_to_grf1, label="STED to GRF1")
            plt.plot(sorted_grf64_to_grf1, label="GRF64 to GRF1")
            plt.plot(sorted_sted_adapted_to_grf1, label="Adapted STED to GRF1")
            plt.ylabel('proportion of distances relative to GRF 1')
            plt.legend()
            plt.savefig(plot_name)
            plt.figure()
            plt.plot(sorted_sted_to_grf1, label="STED to GRF1")
            plt.plot(sorted_sted_adapted_to_grf1, label="Adapted STED to GRF1")
            plt.ylabel('proportion of distances relative to GRF 1')
            plt.legend()
            plt.savefig('plots/sted_sorted_' + tree_size.__str__() + '.png')
            plt.close()

def create_graph(tree_size, number_of_trees, graph_type="zss_to_grf"):
    file_name = 'examples/example_trees_size_' + tree_size.__str__() + '.json'
    plot_name = 'plots/' + graph_type + '_trees_size_' + tree_size.__str__() + ".png"
    if os.path.exists(file_name):
        data = [[[] for _ in range(6)] for _ in range(number_of_trees)]
        with open(file_name) as tree_file:
            tree_list = json.load(tree_file)
        if graph_type == 'zss_to_grf':
            for i in range(0, len(tree_list)):
                j = 0
                for k in [1,64]:
                    key = 'GRF' + str(k)
                    if (key in tree_list[i]):
                        data[i][j] = tree_list[i][key]
                    j = j + 1
                if ('ZSS' in tree_list[i]):
                    data[i][3] = tree_list[i]['ZSS']
                if ('STED' in tree_list[i]):
                    data[i][4] = tree_list[i]['STED']
                if ('STED_adapted' in tree_list[i]):
                    data[i][5] = tree_list[i]['STED_adapted']
            sted_adapted_to_grf1 = [-1 for _ in range(number_of_trees)]
            sted_to_grf1 = [-1 for _ in range(number_of_trees)]
            grf64_to_grf1 = [-1 for _ in range(number_of_trees)]
            for i in range(0, len(data)):
                if (len(data) >= 5):
                    if (data[i][4] and data[i][0] and data[i][2]) and data[i][5]:
                        sted_adapted_to_grf1[i] = float(data[i][5]) / float(data[i][0])
                        sted_to_grf1[i] = float(data[i][4]) / float(data[i][0])
                        grf64_to_grf1[i] = float(data[i][1]) / float(data[i][0])
            sorted_sted_to_grf1 = sorted(sted_to_grf1)
            sorted_grf64_to_grf1 = [x for _,x in sorted(zip(sorted_sted_to_grf1,grf64_to_grf1))]
            sorted_sted_adapted_to_grf1 = sorted(sted_adapted_to_grf1)
            if len(sorted_sted_to_grf1) > 0 :
                index = len(sorted_sted_to_grf1) - 1
                maximum = max(np.amax(sorted_sted_to_grf1), np.amax(sorted_grf64_to_grf1), np.amax(sorted_sted_adapted_to_grf1))
                plt.ylim(0, max(2.5, 0.2 + maximum))
                plt.plot(sorted_sted_to_grf1, label="STED to GRF1")
                plt.plot(sorted_grf64_to_grf1, label="GRF64 to GRF1")
                plt.plot(sorted_sted_adapted_to_grf1, label="Adapted STED to GRF1")
                plt.ylabel('proportion of distances relative to GRF 1')
                plt.legend()
                plt.savefig(plot_name)
                plt.figure()
                plt.plot(sorted_sted_to_grf1, label="STED to GRF1")
                plt.plot(sorted_sted_adapted_to_grf1, label="Adapted STED to GRF1")
                plt.ylabel('proportion of distances relative to GRF 1')
                plt.legend()
                plt.savefig('plots/sted_sorted_' + tree_size.__str__() + '.png')
                plt.close()
        elif graph_type == 'zss':
            zss_0 = [-1 for _ in range(number_of_trees)]
            zss_0_a = [-1 for _ in range(number_of_trees)]
            ated = [-1 for _ in range(number_of_trees)]
            ated_a = [-1 for _ in range(number_of_trees)]
            sted = [-1 for _ in range(number_of_trees)]
            sted_a = [-1 for _ in range(number_of_trees)]
            for i in range(0, len(tree_list)):
                if ('CTED' in tree_list[i]):
                    zss_0[i] = tree_list[i]['CTED'].get('cost') / float(tree_size)
                if ('CTED_a' in tree_list[i]):
                    zss_0_a[i] = tree_list[i]['CTED_a'].get('cost') / float(tree_size)
                if ('ATED' in tree_list[i]):
                    ated[i] = tree_list[i]['ATED'].get('cost') / float(tree_size)
                if ('ATED_a' in tree_list[i]):
                    ated_a[i] = tree_list[i]['ATED_a'].get('cost') / float(tree_size)
                if ('STED' in tree_list[i]):
                    sted[i] = tree_list[i]['STED'].get('cost') / float(tree_size)
                if ('STED_a' in tree_list[i]):
                    sted_a[i] = tree_list[i]['STED_a'].get('cost') / float(tree_size)
            s_zss_0 = sorted(zss_0)
            s_zss_0_a = [x for _,x in sorted(zip(s_zss_0,zss_0_a))]
            s_ated = [x for _,x in sorted(zip(s_zss_0,ated))]
            s_ated_a = [x for _,x in sorted(zip(s_zss_0,ated_a))]
            s_sted = [x for _,x in sorted(zip(s_zss_0,sted))]
            s_sted_a = [x for _,x in sorted(zip(s_zss_0,sted_a))]
            s_zss_lin = [(x+y)/2 for x,y in zip(s_zss_0, s_sted)]
            s_zss_2_0_5 = [2*x-y for x,y in zip(s_ated, s_zss_0)]
            maximum = max(np.amax(sted), np.amax(sted_a))
            plt.ylim(0, maximum + 0.2)
            plt.plot(s_zss_0, label="CTED")
            plt.plot(s_zss_0_a, label="CTED adapted")
            plt.plot(s_ated, label="ATED")
            plt.plot(s_ated_a, label="ATED adapted")
            plt.plot(s_sted, label="STED")
            plt.plot(s_sted_a, label="STED adapted")
            plt.ylabel('different distance measures')
            plt.legend()
            plt.savefig(plot_name)
            plt.close()
        elif graph_type == 'zss_difference':
            zss_0 = [-1 for _ in range(number_of_trees)]
            ated = [-1 for _ in range(number_of_trees)]
            sted = [-1 for _ in range(number_of_trees)]
            for i in range(0, len(tree_list)):
                if 'CTED' in tree_list[i] and 'CTED_a' in tree_list[i]:
                    zss_0[i] = tree_list[i]['CTED'].get('cost') - tree_list[i]['CTED_a'].get('cost')
                if 'ATED' in tree_list[i] and 'ATED_a' in tree_list[i]:
                    ated[i] = tree_list[i]['ATED'].get('cost') - tree_list[i]['ATED_a'].get('cost')
                if 'STED' in tree_list[i] and 'STED_a' in tree_list[i]:
                    sted[i] = tree_list[i]['STED'].get('cost') - tree_list[i]['STED_a'].get('cost')
            s_zss_0 = sorted(zss_0)
            s_ated = [x for _,x in sorted(zip(s_zss_0,ated))]
            s_sted = [x for _,x in sorted(zip(s_zss_0,sted))]
            maximum = max(np.amax(sted), np.amax(ated), np.amax(zss_0))
            minimum = min(np.amin(sted), np.amin(ated), np.amin(zss_0))
            plt.ylim(minimum -0.2, maximum + 0.2)
            plt.plot(s_zss_0, label="Differences CTED and adapted")
            plt.plot(s_ated, label="Differences ATED and adapted")
            plt.plot(s_sted, label="Differences STED and adapted")
            plt.ylabel('different distance measures')
            plt.legend()
            plt.savefig(plot_name)
            plt.close()
        elif graph_type == 'zss_differences_adapted':
            zss_0 = [-1 for _ in range(number_of_trees)]
            zss_0_a = [-1 for _ in range(number_of_trees)]
            ated = [-1 for _ in range(number_of_trees)]
            ated_a = [-1 for _ in range(number_of_trees)]
            sted = [-1 for _ in range(number_of_trees)]
            sted_a = [-1 for _ in range(number_of_trees)]
            for i in range(0, len(tree_list)):
                if 'CTED' in tree_list[i] and 'CTED_a' in tree_list[i]:
                    zss_0[i] = tree_list[i]['CTED'].get('cost')
                    zss_0_a[i] = tree_list[i]['CTED_a'].get('cost')
                if 'ATED' in tree_list[i] and 'ATED_a' in tree_list[i]:
                    ated[i] = tree_list[i]['ATED'].get('cost')
                    ated_a[i] = tree_list[i]['ATED_a'].get('cost')
                if 'STED' in tree_list[i] and 'STED_a' in tree_list[i]:
                    sted[i] = tree_list[i]['STED'].get('cost')
                    sted_a[i] = tree_list[i]['STED_a'].get('cost')
            s_zss_0 = sorted(zss_0)
            s_zss_0_a = [x for _,x in sorted(zip(s_zss_0,zss_0_a))]
            s_ated = sorted(ated)
            s_ated_a = [x for _,x in sorted(zip(s_ated,ated_a))]
            s_sted = sorted(sted)
            s_sted_a = [x for _,x in sorted(zip(s_sted,sted_a))]
            maximum = max(np.amax(zss_0), np.amax(zss_0_a))
            minimum = min(np.amin(zss_0), np.amin(zss_0_a))
            plt.ylim(minimum -0.2, maximum + 0.2)
            plt.plot(zss_0, label="CTED")
            plt.plot(zss_0_a, label="CTED adapted")
            plt.ylabel('different distance measures')
            plt.legend()
            plt.savefig('plots/zss0_sorted_' + tree_size.__str__() + '.png')
            plt.close()
            maximum = max(np.amax(ated), np.amax(ated_a))
            minimum = min(np.amin(ated), np.amin(ated_a))
            plt.ylim(minimum -0.2, maximum + 0.2)
            plt.plot(ated, label="ATED")
            plt.plot(ated_a, label="ATED adapted")
            plt.ylabel('different distance measures')
            plt.legend()
            plt.savefig('plots/zss0_5_sorted_' + tree_size.__str__() + '.png')
            plt.close()
            maximum = max(np.amax(sted), np.amax(sted_a))
            minimum = min(np.amin(sted), np.amin(sted_a))
            plt.ylim(minimum -0.2, maximum + 0.2)
            plt.plot(sted, label="STED")
            plt.plot(sted_a, label="STED adapted")
            plt.ylabel('different distance measures')
            plt.legend()
            plt.savefig('plots/sted_sorted_' + tree_size.__str__() + '.png')
            plt.close()
        elif graph_type == 'low_grf_high_ted':
            ated = [-1 for _ in range(number_of_trees)]
            grf_1 = [-1 for _ in range(number_of_trees)]
            for i in range(0, min(len(tree_list), number_of_trees)):
               # key = 'GRF' + str(k)
                if ('GRF1' in tree_list[i]):
                    if isinstance(tree_list[i]['GRF1'], dict) and 'cost' in tree_list[i]['GRF1']:
                        #print(i, tree_list[i]['GRF1'].keys(), tree_list[i]['GRF1']) 
                        grf_1[i] = tree_list[i]['GRF1'].get('cost') / float(tree_size)
                    elif isinstance(tree_list[i]['GRF1'],(int,float)):
                        grf_1[i] = tree_list[i]['GRF1']
                if ('ATED' in tree_list[i]):
                    ated[i] = tree_list[i]['ATED'].get('cost') / float(tree_size)
            s_grf_1 = sorted(grf_1)
            s_ated = [x for _,x in sorted(zip(grf_1,ated))]
            low_grf_1 = [s_grf_1[i] for i in range(0,31)];
            low_ated = [s_ated[i] for i in range(0,31)];
            high_grf_1 = [s_grf_1[i] for i in range(269,300)];
            high_ated = [s_ated[i] for i in range(269,300)];
            
            if len(low_grf_1) > 0 and len(low_ated) > 10:
                maximum = max(np.amax(low_grf_1), np.amax(low_ated))
                plot_name = 'plots/low_grf_corr_ated.png'
                plt.figure(1)
                plt.grid(True)
                plt.ylim(0, max(2, 0.2 + maximum)) 
                plt.yticks([0, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2])
                plt.xlim(0, 30) 
                plt.xticks([0,5,10,15,20,25,30])
                plt.plot(low_grf_1, label="lowest gRFs")
                plt.plot(low_ated, label="corresponding ATED")
                plt.plot((0,30),(min(ated),min(ated)),'--', label="lowest ATED 0,5")
                plt.plot((0,30),(max(ated),max(ated)),'--', label="highest ATED 0,5")
                plt.ylabel('distance values')
                plt.xlabel('example count')
                plt.legend()
                plt.savefig(plot_name)
                #plt.figure()
                plt.close()
            if len(high_grf_1) > 0 and len(high_ated) > 10:
                maximum = max(np.amax(high_grf_1), np.amax(high_ated))
                plot_name = 'plots/high_grf_corr_ated.png'
                plt.figure(2)
                plt.grid(True)
                plt.ylim(0, max(2, 0.2 + maximum)) 
                plt.yticks([0, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2])
                plt.xlim(0, 30)
                plt.xticks([0,5,10,15,20,25,30])
                plt.plot(high_grf_1, label="highest gRFs")
                plt.plot(high_ated, label="corresponding ATED")
                plt.plot((0,30),(min(ated),min(ated)),'--', label="lowest ATED 0,5")
                plt.plot((0,30),(max(ated),max(ated)),'--', label="highes ATED 0,5")
                plt.ylabel('distance values')
                plt.xlabel('example count')
                plt.legend()
                plt.savefig(plot_name)
                plt.figure()
                plt.close()
            if len(s_grf_1) > 0 and len(s_ated) > 10:
                maximum = max(np.amax(s_ated), np.amax(s_ated))
                plot_name = 'plots/all_examples_grf_corr_ated.png'
                plt.figure(3,(24,8))
                plt.grid(True)
                plt.ylim(0, max(2, 0.2 + maximum)) 
                plt.yticks([0, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2])
                plt.xlim(0, 300) 
                plt.xticks([0,30,75,150,225,270,300])
                plt.plot(s_grf_1, label="all gRFs ascending")
                plt.plot(s_ated, label="corresponding ATED")
                plt.plot((0,300),(min(ated),min(ated)),'--', label="lowest ATED 0,5")
                plt.plot((0,300),(max(ated),max(ated)),'--', label="highes ATED 0,5")
                plt.ylabel('distance values')
                plt.xlabel('example count')
                plt.legend()
                plt.savefig(plot_name)
                plt.figure()
                plt.close()
            
            rs_ated = sorted(ated)
            rs_grf_1 = [x for _,x in sorted(zip(ated,grf_1))]
            if len(rs_ated) > 0 and len(rs_grf_1) > 10:
                maximum = max(np.amax(rs_ated), np.amax(rs_ated))
                plot_name = 'plots/all_examples_ated_corr_grf.png'
                plt.figure(4,(24,8))
                plt.grid(True)
                plt.ylim(0, max(2, 0.2 + maximum)) 
                plt.yticks([0, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2])
                plt.xlim(0, 300) 
                plt.xticks([0,30,75,150,225,270,300])
                plt.plot(rs_grf_1, label="corresponding gRFs")
                plt.plot(rs_ated, label="all ATED ascending")
                plt.plot((0,300),(min(rs_grf_1),min(rs_grf_1)),'--', label="lowest gRF")
                plt.plot((0,300),(max(rs_grf_1),max(rs_grf_1)),'--', label="highes gRF")
                plt.ylabel('distance values')
                plt.xlabel('example count')
                plt.legend()
                plt.savefig(plot_name)
                plt.figure()
                plt.close()

def create_time_graph():
    k_array = [4,5,6,7,8,9,10,11,12,16,20,24,32,40,48,64,128,192,256]
    ar_zss_0 = []
    ar_zss_0_a = []
    ar_ated = []
    ar_ated_a = []
    ar_sted = []
    ar_sted_a = []
    ar_grf1 = []
    ar_grf64 = []
    for k in k_array:
        zss_0 = zss_0_a = ated = ated_a = sted = sted_a = grf1 = grf64 = {'time': 0, 'count': 0}
        file_name = 'examples/example_trees_size_' + k.__str__() + '.json'
        if os.path.exists(file_name):
            with open(file_name) as tree_file:
                tree_list = json.load(tree_file)
            for tree in tree_list:
                if 'GRF1' in tree and tree['GRF1'].get('time'):
                    grf1 = {'time': grf1.get('time') + tree['GRF1'].get('time'), 'count': grf1.get('count') + 1}
                if 'GRF64' in tree and tree['GRF64'].get('time'):
                    grf64 = {'time': grf64.get('time') + tree['GRF64'].get('time')
                        , 'count': grf64.get('count') + 1}
                if 'CTED' in tree and tree['CTED'].get('time'):
                    zss_0 = {'time': zss_0.get('time') + tree['CTED'].get('time')
                        , 'count': zss_0.get('count') + 1}
                if 'CTED_a' in tree and tree['CTED_a'].get('time'):
                    zss_0_a = {'time': zss_0_a.get('time') + tree['CTED_a'].get('time')
                        , 'count': zss_0_a.get('count') + 1}
                if 'ATED' in tree and tree['ATED'].get('time'):
                    ated = {'time': zss_0.get('time') + tree['ATED'].get('time')
                        , 'count': ated.get('count') + 1}
                if 'ATED_a' in tree and tree['ATED_a'].get('time'):
                    ated_a = {'time': ated_a.get('time') + tree['ATED_a'].get('time')
                        , 'count': ated_a.get('count') + 1}
                if 'STED' in tree and tree['STED'].get('time'):
                    sted = {'time': sted.get('time') + tree['STED'].get('time')
                        , 'count': sted.get('count') + 1}
                if 'STED_a' in tree and tree['STED_a'].get('time'):
                    sted_a =  {'time': sted_a.get('time') + tree['STED_a'].get('time')
                        , 'count': sted_a.get('count') + 1}

            if zss_0.get('count'):
                 ar_zss_0.append(zss_0.get('time') / zss_0.get('count'))
            if zss_0_a.get('count'):
                 ar_zss_0_a.append(zss_0_a.get('time') / zss_0_a.get('count'))
            if ated.get('count'):
                 ar_ated.append(zss_0.get('time') / ated.get('count'))
            if ated_a.get('count'):
                 ar_ated_a.append(ated_a.get('time') / ated_a.get('count'))
            if sted.get('count'):
                ar_sted.append(sted.get('time') / sted.get('count'))
            if sted_a.get('count'):
                ar_sted_a.append(sted_a.get('time') / sted_a.get('count'))
            if grf1.get('count') > 5:
                ar_grf1.append(grf1.get('time') / grf1.get('count'))
            if grf64.get('count') > 5:
                ar_grf64.append(grf64.get('time') / grf64.get('count'))
    maximum = max(np.amax(ar_grf64), np.amax(ar_grf1), np.amax(ar_sted_a), np.amax(ar_sted))

    # time plot all
    plt.figure()
    plt.ylim(0, 1000)
    plt.plot(k_array, ar_zss_0, label="CTED")
    plt.plot(k_array, ar_zss_0_a, label="CTED adapted")
    plt.plot(k_array, ar_ated, label="ATED")
    plt.plot(k_array, ar_ated_a, label="ATED adapted")
    plt.plot(k_array, ar_sted, label="STED")
    plt.plot(k_array, ar_sted_a, label="STED adapted")
    plt.plot(k_array[0:len(ar_grf1)], ar_grf1, label="gRF 1")
    plt.plot(k_array[0:len(ar_grf64)], ar_grf64, label="gRF 64")
    plt.ylabel('time taken for the different approaches')
    plt.legend()
    plt.savefig('plots/time_plot_all.png')
    plt.figure()
    plt.close()

    # time plot zss
    plt.figure()
    plt.ylim(0, 1000)
    plt.plot(k_array, ar_zss_0, label="CTED")
    plt.plot(k_array, ar_zss_0_a, label="CTED adapted")
    plt.plot(k_array, ar_ated, label="ATED")
    plt.plot(k_array, ar_ated_a, label="ATED adapted")
    plt.plot(k_array, ar_sted, label="STED")
    plt.plot(k_array, ar_sted_a, label="STED adapted")
    plt.ylabel('time taken for the different approaches')
    plt.legend()
    plt.savefig('plots/time_plot_zss.png')
    plt.close()


    # time plot grf / zss
    plt.figure()
    plt.ylim(0, 1000)
    plt.plot(k_array, ar_sted, label="Tree Edit Distance")
    plt.plot(k_array[0:len(ar_grf1)], ar_grf1, label="generalized Robinson Foulds")
    plt.ylabel('average time taken for the different approaches (in s)')
    plt.xlabel('number of leaves on each example tree')
    plt.legend()
    plt.savefig('plots/time_plot_all.png')
    plt.figure()
    plt.close()

