from Coordinator.transmitter import ProfileTransmitter


if __name__ == '__main__':
    transmitt = ProfileTransmitter(db_name='analyzed')
    transmitt.run()
