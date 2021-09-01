# WESLEY WONG KEE HAN
# TP059618


def display_main_menu():
    while True:  # while loop used to repeat input action if users enter an invalid action.
        print("""1. Register A New Patient
2. Search & Update Patient Details
3. View Statistics
4. Exit""")
        option = input("Action: ")
        try:
            option = int(option)
            if option == 1:
                register_new_patient()
            elif option == 2:
                search_and_update_patient_details()
            elif option == 3:
                view_statistics()
            elif option == 4:
                exit()
            else:
                print("Invalid Action")
                continue
        except ValueError:
            print("Numerical Error")
            continue


def register_new_patient():
    while True:  # while loop used to repeat registration.
        patients = []
        details = []
        print("Enter New Patient Details or Enter 'Exit' to Return to Main Menu")
        # every input is upper cased to prevent case-sensitive error.
        name = str(input("Name: ")).upper()
        if name == "EXIT":
            display_main_menu()
        else:
            details.append(name)
        group = str(input("Group: ")).upper()
        zone = str(input("Zone: ")).upper()
        details.append(group)
        details.append(zone)
        while True:  # while loop used to repeat phone number input if users enter an invalid action.
            contact_number = input("Phone Number: +601")
            # assuming patients are only necessary to input mobile phone number instead of home number.
            try:
                if 8 <= len(contact_number) <= 9:
                    contact_number = int(contact_number)
                    details.append('01' + str(contact_number))
                    break
                else:  # error due to invalid length of phone number.
                    print("Please Enter A Valid Phone Number")
                    continue
            except ValueError:  # error due to alphabetic input.
                print("Please Enter A Valid Phone Number")
                continue
        patient_id = patient_count_increment(group, zone)  # increase total amount of patient registered.
        details.append(patient_id)
        first_test_result = input("Result of First Test: ").upper()
        details.append(first_test_result)
        follow_up = decision_table(1, first_test_result, group)  # decide what action to do next based on table.
        if not follow_up:
            # patient tested positive, no followup required, hence the need to generate case id and track status.
            # possible status: ACTIVE RECOVERED DECEASED
            second_test_result = "Not Required"
            third_test_result = "Not Required"
            details.append(second_test_result)
            details.append(third_test_result)
            case_id = case_count_increment()  # generate case id, and increase total amount of cases.
            details.append(case_id)
            status = "ACTIVE"
            details.append(status)
        else:
            # patient tested negative, followup required, case id and status are not generated.
            second_test_result = "To Be Determined"
            third_test_result = "To Be Determined"
            details.append(second_test_result)
            details.append(third_test_result)
            details.append('')
            details.append('')
        patients.append(details)
        with open("database.txt", "a") as database:  # store info into file.
            for data in patients:
                database.write(
                    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s|"
                    % (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9]))
        while True:  # while loop used to repeat phone number input if users enter an invalid action.
            print("Enter '1' To Register New Patient or 'Exit' to Return to Main Menu")
            option = input("Action: ")
            if option == "1":
                break
            elif option.upper() == "EXIT":
                display_main_menu()
            else:
                print("Invalid Action")
                continue


def search_and_update_patient_details():
    while True:  # while loop used to repeat input when result does not match
        all_patients = []
        searching_patients = []
        user_found = False  # variable used to break out of loop once a patient details is matched.
        search_keyword = input("Please Enter Patient's Name, Patient ID or Case ID to Search for Details "
                               "or 'Exit' to Return to Main Menu: ").upper()
        if search_keyword == 'EXIT':
            display_main_menu()
        with open("database.txt", "r") as database:
            for data in database:
                for patients in data.split('|'):  # nested loop to retrieve entire data from database to a empty list.
                    all_patient_details = []
                    if patients != '':  # refer to limitations
                        ''' 
                        due to database always having '|' as divider, when '|' splits, 
                        last element would be an empty list and throws an error,
                        when the system tries to access indexes.
                        hence, line 114 is the fix to this bug.
                        '''
                        for details in patients.split(','):
                            all_patient_details.append(details)
                        all_patients.append(all_patient_details)
                for patients in data.split('|'):  # nested loop to retrieve only currently searching data.
                    patient_details = []
                    if patients != '':  # refer to limitations
                        ''' 
                        due to database always having '|' as divider, when '|' splits, 
                        last element would be an empty list and throws an error,
                        when the system tries to access indexes.
                        hence, line 126 is the fix to this bug.
                        '''
                        patient_id = ''
                        case_id = ''
                        for details in patients.split(','):
                            patient_details.append(details)
                            if '-' in details:
                                patient_id = details
                            elif 'C/' in details:
                                case_id = details
                        searching_patients.append(patient_details)
                        index_patients = (len(searching_patients) - 1)
                        ''' 
                        index_patients is used to keep track of
                        the position of currently searching patient data in the list.
                        '''
                        if search_keyword == patient_details[0] or search_keyword == patient_id \
                                or search_keyword == case_id:  # search for patient
                            display_details(patient_details)  # display all patient's details when result is matched.
                            user_found = True
                            completion = False  # used to break out of loop once patient details is updated.
                            while True:  # update patient's details.
                                if completion:
                                    break
                                update = input("Please Enter '1' to Update Patient's Details or 'Back' to "
                                               "Search for Next Patient: ").upper()
                                if update == 'BACK':
                                    break
                                elif update == '1':
                                    if patient_details[9] == 'ACTIVE':
                                        '''
                                        the 9th index is status of patient.
                                        for a negatively tested patient, the 9th element would be empty.
                                        if a patient's 9th element isn't empty, 
                                        means they are positively tested
                                        '''
                                        while True:
                                            if completion:
                                                break
                                            option = input('''Update Patient's Details
1. Status (Active/Recovered/Deceased)
Field: ''')
                                            if option == '1':
                                                while True:
                                                    updated_status = input("New Status: ").upper()
                                                    if updated_status == patient_details[9]:
                                                        print("New status must be different from old status")
                                                        continue
                                                    else:
                                                        patient_details[9] = updated_status
                                                        all_patients[index_patients] = \
                                                            searching_patients[index_patients]
                                                        with open("database.txt", "w") as database_write:
                                                            for info in all_patients:
                                                                database_write.write(
                                                                    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s|"
                                                                    % (info[0], info[1], info[2], info[3], info[4],
                                                                       info[5], info[6], info[7], info[8], info[9]))
                                                        display_details(patient_details)
                                                        completion = True  # update process successful.
                                                        break
                                            else:
                                                print("Invalid Action")
                                                continue
                                    elif patient_details[6] == "To Be Determined" \
                                            and patient_details[7] == "To Be Determined":
                                        # patient has only gone through first test.
                                        completion = False
                                        while True:
                                            option = input('''Update Patient's Details
1. Second Test Result
Field: ''')
                                            if option == '1':
                                                updated_second_test_result = input("Second Test Result: ").upper()
                                                if updated_second_test_result == 'POSITIVE':
                                                    # generate case id and status.
                                                    patient_details[7] = 'Not Required'
                                                    patient_details[8] = case_count_increment()
                                                    patient_details[9] = 'ACTIVE'
                                                decision_table(2, updated_second_test_result, patient_details[1])
                                                # determine next action.
                                                patient_details[6] = updated_second_test_result
                                                all_patients[index_patients] = searching_patients[index_patients]
                                                with open("database.txt", "w") as database_write:
                                                    for info in all_patients:
                                                        database_write.write(
                                                            "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s|"
                                                            % (info[0], info[1], info[2], info[3], info[4], info[5],
                                                               info[6], info[7], info[8], info[9]))
                                                display_details(patient_details)
                                                completion = True
                                                break
                                            else:
                                                print("Invalid Action")
                                                continue
                                    elif patient_details[6] != "To Be Determined" \
                                            and patient_details[7] == "To Be Determined":
                                        # patient has gone through first and second test.
                                        completion = False
                                        while True:
                                            option = input('''Update Patient's Details
1. Third Test Result
Field: ''')
                                            if option == '1':
                                                updated_third_test_result = input("Third Test Result: ").upper()
                                                if updated_third_test_result == 'POSITIVE':
                                                    # generate case id and status.
                                                    patient_details[8] = case_count_increment()
                                                    patient_details[9] = 'ACTIVE'
                                                decision_table(3, updated_third_test_result, patient_details[1])
                                                patient_details[7] = updated_third_test_result
                                                all_patients[index_patients] = searching_patients[index_patients]
                                                with open("database.txt", "w") as database_write:
                                                    for info in all_patients:
                                                        database_write.write(
                                                            "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s|"
                                                            % (info[0], info[1], info[2], info[3], info[4], info[5],
                                                               info[6], info[7], info[8], info[9]))
                                                display_details(patient_details)
                                                completion = True
                                                break
                                            else:
                                                print("Invalid Action")
                                                continue
                                    else:  # patient is either healthy, recovered or deceased.
                                        print("Unable to update any details, patient's case is closed")
                                else:
                                    print("Invalid Action")
                                    continue
                if not user_found:  # patient details don't match.
                    print("Patient not found")
                    continue


def view_statistics():
    active_case = 0
    recovered_case = 0
    deceased_case = 0
    total_test = 0
    ato = 0
    acc = 0
    aeo = 0
    sid = 0
    ahs = 0
    a = 0
    b = 0
    c = 0
    d = 0
    with open("patient_count.txt", "r") as patient_tracker:
        patient_count = int(patient_tracker.read())
    with open("case_count.txt", "r") as case_tracker:
        case_count = int(case_tracker.read())
    print("Total Patients Registered: " + str(patient_count))  # convert integer to string for concatenation.
    print("Total Cases: " + str(case_count))  # convert integer to string for concatenation.
    with open("database.txt", "r") as database:  # search database for all possible cases' status.
        for data in database:
            for patients in data.split('|'):
                patient_details = []
                if patients != '':  # refer to limitations
                    ''' 
                    due to database always having '|' as divider, when '|' splits, 
                    last element would be an empty list and throws an error,
                    when the system tries to access indexes.
                    hence, line 289 is the fix to this bug.
                    '''
                    for details in patients.split(','):
                        patient_details.append(details)
                    for info in patient_details:  # accessing every single element in the patient list.
                        if info == 'ACTIVE':
                            active_case += 1
                        elif info == 'RECOVERED':
                            recovered_case += 1
                        elif info == 'DECEASED':
                            deceased_case += 1
                        elif info == 'POSITIVE' or info == 'NEGATIVE':
                            total_test += 1
                    # total amount of cases = active_cases + recovered_cases + deceased_cases.
                    if patient_details[8] != '':
                        # including cases that are tested positive currently and in the past.
                        if patient_details[1] == 'ATO':
                            ato += 1
                        elif patient_details[1] == 'ACC':
                            acc += 1
                        elif patient_details[1] == 'AEO':
                            aeo += 1
                        elif patient_details[1] == 'SID':
                            sid += 1
                        elif patient_details[1] == 'AHS':
                            ahs += 1
                    # ato + acc + aeo + sid + ahs also equals to total amount of cases.
                    if patient_details[9] == 'ACTIVE':
                        # currently active cases only, past positive cases are excluded.
                        if patient_details[2] == 'A':
                            a += 1
                        elif patient_details[2] == 'B':
                            b += 1
                        elif patient_details[2] == 'C':
                            c += 1
                        elif patient_details[2] == 'D':
                            d += 1
                    # a + b + c + d = total active cases.
    print("Total Active Cases: " + str(active_case))  # convert integer to string for concatenation.
    print("Total Recovered Cases: " + str(recovered_case))
    print("Total Deceased Cases: " + str(deceased_case))
    print("Total Amount of Test Carried out: " + str(total_test))
    print("Patients Tested Positive By Groups:")
    print("- ATO " + str(ato))
    print("- ACC " + str(acc))
    print("- AEO " + str(aeo))
    print("- SID " + str(sid))
    print("- AHS " + str(ahs))
    print("Active Cases By Zones:")
    print("- A " + str(a))
    print("- B " + str(b))
    print("- C " + str(c))
    print("- D " + str(d))
    while True:
        print("Enter 'Exit' to Return to Main Menu")
        option = input("Action: ")
        if option.upper() == "EXIT":
            display_main_menu()
        else:
            print("Invalid Action")
            continue


def patient_count_increment(patient_group, patient_zone):
    with open("patient_count.txt", "r") as patient_tracker:  # increase total amount of patient registered.
        patient_count = int(patient_tracker.read())
        patient_count += 1
    with open("patient_count.txt", "w") as patient_tracker:
        patient_tracker.write(str(patient_count))
    patient_id = patient_group + '-' + str(patient_count) + '-' + patient_zone  # generate unique patient id.
    return patient_id


def case_count_increment():
    with open("case_count.txt", "r") as case_tracker:  # increase total amount of cases.
        case_count = int(case_tracker.read())
        case_count += 1
    with open("case_count.txt", "w") as case_tracker:
        case_tracker.write(str(case_count))
    case_id = 'C/' + str(case_count)  # generate unique case id.
    return case_id


def display_details(details):  # output patient's details upon successful search or after updating details.
    print("Name: " + details[0])
    print("Group: " + details[1])
    print("Zone: " + details[2])
    print("Phone Number: " + details[3])
    print("Patient ID: " + details[4])
    print("First Test: " + details[5])
    print("Second Test: " + details[6])
    print("Third Test: " + details[7])
    if details[8] != '':  # 9th element isn't empty, means the patient is infected as has case_id generated
        print("Case ID: " + details[8])
        print("Status: " + details[9])


def decision_table(order, test_result, patient_group):  # decides next action based on patients' group and test results.
    follow_up = ''
    if patient_group != 'AHS' and test_result == 'POSITIVE':
        if order == 1:
            print("QNHF - Quarantine in Hospital Normal Ward (No Follow-Up Test Required)")
        elif order == 2 or order == 3:
            print("QNHF - Quarantine in Hospital ICU (No Follow-Up Test Required)")
        follow_up = False
    elif patient_group == 'AHS' and test_result == 'POSITIVE':
        print("HQHF - Home Quarantine (No Follow-Up Test Required)")
        follow_up = False
    elif patient_group != 'AHS' and patient_group != 'SID' and test_result == 'NEGATIVE' and (order == 1 or order == 2):
        print("QDFR - Quarantine in Designated Centres (Follow-Up Test Required)")
        follow_up = True
    elif patient_group == 'SID' and test_result == 'NEGATIVE' and (order == 1 or order == 2):
        print("HQFR - Home Quarantine (Follow-Up Test Required)")
        follow_up = True
    elif patient_group == 'AHS' and test_result == 'NEGATIVE' and (order == 1 or order == 2):
        print("CWFR - Continue Working (Follow-Up Test Required)")
        follow_up = True
    elif patient_group != 'AHS' and test_result == 'NEGATIVE' and order == 3:
        print("RU - Allow to reunion with family")
        follow_up = False
    elif patient_group == 'AHS' and test_result == 'NEGATIVE' and order == 3:
        print("CW - Continue Working")
        follow_up = False
    return follow_up


display_main_menu()
