import torch 
from readConcepts import ConceptData

from CNNNetwork import Net

import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F

from constt import *

import utils, logics


print ("ROOT ", ROOT)

from sklearn.metrics import confusion_matrix
import numpy as np 


import yaml
import torchvision
from torchvision import transforms

# trans = transforms.Compose([        
#                                     # transforms.CenterCrop((178, 178)),
#                                     # transforms.Resize(128),
#                                     # transforms.RandomRotation(20),
#                                     transforms.ToTensor()
#                                     # transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))

#                                     ])






def train(allConceptsFuncs):

    resultDict = {}
    resultConfMat = {}
    for CONCEPT_NAME in allConceptsFuncs :



        # if allConceptsFuncs[CONCEPT_NAME][0] < COUNT_THRESHOLD :
        #     continue 

        # if CONCEPT_NAME != "concept_box_below" :
        #     continue

        print ("--"*20)
        print ("TRAINING -- CONCEPT_NAME :", CONCEPT_NAME)



        dataset = ConceptData(ROOT, CONCEPT_NAME, seed=SEED, transform=None, pos_limit=POS_LIMIT, neg_limit=NEG_LIMIT, selectPossible=SELECT_POSSIBLE)
        # TRAIN_RATIO = 0.2   -- from constt

        trainsize = int(dataset.__len__()*TRAIN_RATIO)
        testsize = dataset.__len__() - trainsize
        train_set, val_set = torch.utils.data.random_split(dataset, [trainsize, testsize])


        print (train_set.__len__(), val_set.__len__())


        trainloader = torch.utils.data.DataLoader(train_set, batch_size=BATCH_SIZE,
                                                  shuffle=True, num_workers=2)
        testloader = torch.utils.data.DataLoader(val_set, batch_size=BATCH_SIZE,
                                                 shuffle=False, num_workers=2)






        net = Net()

        criterion = nn.CrossEntropyLoss()
        # optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
        optimizer = optim.Adagrad(net.parameters(), lr=0.01, lr_decay=0, weight_decay=0.05, initial_accumulator_value=0, eps=1e-10)



        def test (testloader):
            correct = 0
            total = 0
            all_labels = None
            all_predictions = None
            conf_mat = np.zeros((2,2)) 


            with torch.no_grad():
                for data in testloader:
                    inputs, labels = data
                    inputs = inputs.permute(0,3,1,2).float()
                    # inputs = inputs.float()
                    labels = labels.long()


                    outputs = net(inputs)
                    _, predicted = torch.max(outputs.data, 1)
                    total += labels.size(0)
                    correct += (predicted == labels).sum().item()

                    if type(all_labels) == type(labels) :
                        all_labels = torch.cat((all_labels, labels))
                    else :
                        all_labels = labels
                    if type(all_predictions) == type(predicted) :
                        all_predictions = torch.cat((all_predictions, predicted))
                    else :
                        all_predictions = predicted
           
            conf_mat = confusion_matrix(all_labels, all_predictions)
            print (conf_mat)

            print ("DATESET -- \nTrain ", train_set.__len__(), "Test ", val_set.__len__())
            print ("In Train : ", )
            print('Accuracy of the network on test images: %d %%' % (
                100 * correct / total))



            return float(100*correct)/total, conf_mat


        # TRAIN -- 

        try : 
            for epoch in range(EPOCHS):  # loop over the dataset multiple times

                running_loss = 0.0
                for i, data in enumerate(trainloader, 0):
                    inputs, labels = data


                    inputs = inputs.permute(0,3,1,2).float()
                    # inputs = inputs.float()
                    labels = labels.long()

                    # print (inputs.shape)

                    optimizer.zero_grad()

                    outputs = net(inputs)
                    # print (outputs, labels)
                    loss = criterion(outputs, labels)
                    loss.backward()
                    optimizer.step()

                    # print (running_loss)
                    running_loss += loss.item()
                    # if i % 2000 == 1999:    # print every 2000 mini-batches
                    if i%5==0:
                        print('[%d, %5d] loss: %.3f' %
                              (epoch + 1, i + 1, float(loss.item()) ))
                        # running_loss = 0.0
                        # test(testloader)    

                acc, conf_mat = test(testloader)
                resultDict[CONCEPT_NAME] = acc
                resultConfMat[CONCEPT_NAME] = conf_mat
        except :
            print ("Stopped midway..")
        print('Finished Training')
        # TESTING ---- 
        
        PATH = ROOT + "/models/" + str(CONCEPT_NAME) + ".pth"
        torch.save(net.state_dict(), PATH)

    print (resultDict)
    print (resultConfMat)


# allConceptsFuncs = utils.findAllConcepts()

with open('concept_cnt_cell.yaml') as c_fd:
    allConceptsFuncs = yaml.load(c_fd)
#allConceptsFuncs = {
# 'concept_blank_cell_below': [495, 259, 259],
# 'concept_blank_cell_on_left': [458, 296, 296],
# 'concept_box_below': [22, 732, 732],
# 'concept_box_on_left': [17, 737, 737],
# 'concept_box_on_right': [20, 734, 734],
# 'concept_box_on_top': [21, 733, 733],
# 'concept_no_pink_cell_below_m': [567, 187, 187],
# 'concept_no_pink_cell_on_top_m': [573, 181, 181],
# 'concept_no_wall_below_m': [456, 298, 298],
# 'concept_no_wall_on_left_m': [324, 430, 430],
# 'concept_no_wall_on_right_m': [340, 414, 414],
# 'concept_no_wall_on_top_m': [448, 306, 306],
# 'concept_on_pink_cell': [100, 654, 654],
# 'concept_pink_cell_below': [69, 685, 685],
# 'concept_pink_cell_on_left': [67, 687, 687],
# 'concept_pink_cell_on_right': [70, 684, 684],
# 'concept_pink_cell_on_top': [68, 686, 686],
# 'concept_target_on_right': [23, 731, 731],
# 'concept_target_on_top': [24, 730, 730],
# 'concept_wall_above_box': [70, 684, 684],
# 'concept_wall_below': [168, 586, 586],
# 'concept_wall_below_box': [153, 601, 601],
# 'concept_wall_down_left': [41, 713, 713],
# 'concept_wall_down_right': [66, 688, 688],
# 'concept_wall_on_left': [212, 542, 542],
# 'concept_wall_on_left_of_box': [199, 555, 555],
# 'concept_wall_on_right': [199, 555, 555],
# 'concept_wall_on_right_of_box': [169, 585, 585],
# 'concept_wall_on_top': [170, 584, 584],
# 'concept_wall_top_left': [31, 723, 723],
# 'concept_wall_top_right': [52, 702, 702],
# 'concept_wall_up_down_right': [19, 735, 735]
#}

train(allConceptsFuncs)

