import sys

import pywinusb.hid as hid

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: KeyboardLEDControl.exe {0|1}")
        sys.exit(1)

    vendor_id = 0x3434
    product_id = 0x0361

    usage_page = 0xFF60
    usage = 0x63

    target_usage = hid.get_full_usage_id(usage_page, usage)

    all_devices = hid.HidDeviceFilter(vendor_id=vendor_id, product_id=product_id).get_devices()

    if not all_devices:
        print("Can't find target device (vendor_id = 0x%04x)!" % vendor_id)
    else:
        usage_found = False
        for device in all_devices:
            try:
                device.open()
                for report in device.find_output_reports():
                    if target_usage in report:
                        data = [0x07, 0x00, 0x01, int(sys.argv[1])]
                        data += [0x00]*(len(report[target_usage].value)-len(data))
                        report[target_usage] = data
                        report.send()
                        print("Command sent to device\n")
                        usage_found = True
            finally:
                device.close()
        if not usage_found:
            print("The target device was found, but the requested usage does not exist!\n")
