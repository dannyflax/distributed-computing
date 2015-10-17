//
//  ViewController.h
//  Distrubutor
//
//  Created by Taha  on 10/16/15.
//  Copyright © 2015 OSUBoilerMaker. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "TCP_Handler.h"
@interface ViewController : UIViewController <TCP_Delegate>
{
    TCP_Handler *tcpHandler;
}
@end

