Public Class PeterConsole
    Public PricePerLitre As Single = 0.24
    Public PetrolPumped As Single = 0
    Public CurrentCharge As Single = 0
    Public PumpStatus As String = "Replaced"
    Public none As String = ""
    Dim TotalTakings As Single = 0
    Dim TotalPumped As Single = 0

    Public Sub Show_Info_Top(ByVal status, ByVal pumped, ByVal charge)
        LBL_PetrolPumped.Text = "Petrol Pumped: " & pumped & " l"
        LBL_CurrentPrice.Text = "Current Price: £" & charge
        LBL_PumpStatus.Text = "Pump Status: " & status
    End Sub

    Private Sub Set_Totals(ByVal price, ByVal pumped)
        TotalTakings = price
        LBL_TotalTakings.Text = "Total Takings: £" & price
        TotalPumped = pumped
        LBL_TotalPetrolPumped.Text = "Total Petrol Pumped: " & pumped & " l"
    End Sub

    Private Sub Console_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
        'Dim pump As New Pump()
        FRM_Pump.Show()
        TXT_EnterPricePerLitre.Text = PricePerLitre

        ''''''''''''''''''''''''''
        ' Peter's Instructions'''''
        ''''''''''''''''''''''''''
        'Dim PeterInstructions As String
        'PeterInstructions = "Peter is the fail. No, really he is. He does nto have petrol pumps, FOR I HAVE THE PETROL PUMPS. What a loser. HAHAR"
        'LBL_PTR_INSTR.Text = Multiliner(PeterInstructions, 90)

    End Sub

    Private Sub BTN_ZeroPumpDisplay_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles BTN_ZeroPumpDisplay.Click
        If PumpStatus = "Replaced" Then
            TotalTakings += FRM_Pump.CurrentPrice
            TotalPumped += FRM_Pump.PetrolPumped
            FRM_Pump.PetrolPumped = 0
            FRM_Pump.CurrentPrice = 0
            FRM_Pump.Ticks = 0
            Set_Totals(TotalTakings, TotalPumped)
            FRM_Pump.RefreshCounters()
            Show_Info_Top(PumpStatus, FRM_Pump.PetrolPumped, FRM_Pump.CurrentPrice)
        End If
    End Sub

    Private Sub BTN_AlterPricePerLitre_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles BTN_AlterPricePerLitre.Click
        If PumpStatus = "Replaced" Then
            Try
                PricePerLitre = CSng(TXT_EnterPricePerLitre.Text)
                FRM_Pump.SetPPL(PricePerLitre)
            Catch
                PricePerLitre = PricePerLitre
            End Try
        End If
    End Sub

    Private Sub BTN_ResetDayTotal_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles BTN_ResetDayTotal.Click
        Set_Totals(0, 0)
    End Sub
End Class