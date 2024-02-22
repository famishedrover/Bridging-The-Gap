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
with open('concept_cnt_switch.yaml') as c_fd:
    allConceptsFuncs = yaml.load(c_fd)

#allConceptsFuncs = {
# 'concept_above_switch': [25, 953, 953],
# 'concept_box_above': [33, 945, 945],
# 'concept_box_below': [26, 952, 952],
# 'concept_box_left': [22, 956, 956],
# 'concept_box_right': [25, 953, 953],
# 'concept_empty_above': [728, 250, 250],
# 'concept_empty_below': [672, 306, 306],
# 'concept_empty_left': [644, 334, 334],
# 'concept_empty_right': [629, 349, 349],
# 'concept_left_switch': [30, 948, 948],
# 'concept_switch_on': [332, 646, 646],
# 'concept_target_above': [29, 949, 949],
# 'concept_target_below': [29, 949, 949],
# 'concept_target_left': [27, 951, 951],
# 'concept_target_right': [28, 950, 950],
# 'concept_wall_above': [188, 790, 790],
# 'concept_wall_below': [226, 752, 752],
# 'concept_wall_left': [285, 693, 693],
# 'concept_wall_left_below_ofbox': [51, 927, 927],
# 'concept_wall_right': [266, 712, 712]}

train(allConceptsFuncs)

