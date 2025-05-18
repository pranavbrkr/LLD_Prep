Enums
Different vehicle types

Classes
Vehicle: license plate, type and ticket assigned
Parking spot: spot id, type and occupied flag | is Available | occupy | vacate
Parking level: list of spots, level number | get available spot
Parking lot: list of levels | get available spot
Ticket: vehicle, level, spot, intime, outtime | close ticket
TicketFactory (For creation of ticket): | createTicket
ParkingSpotManager (For finding, assigning and vacating spots): parking lot | find, occupy, vacate
TicketManager (For ticket creation and closing): tickets | issue ticket, close ticket
PricingStrategy <- FlatStrategy, HourlyStrategy: | calculate price
PriceCalculator (For price calculation): strategy | calculate price
PaymentStrategy <- CardPayment, CashPayment: | pay the amount
PaymentManager (To handle payment): payment strategy, pricing strategy | calculate amount, strategy payment, perform payment(use prev two methods)
ParkingLotService (To orchestrate all the functionalities): parking spot manager, ticket managet | park vehicle, unpark vehicle