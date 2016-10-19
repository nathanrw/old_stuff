<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class FRM_Pump
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        If disposing AndAlso components IsNot Nothing Then
            components.Dispose()
        End If
        MyBase.Dispose(disposing)
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.components = New System.ComponentModel.Container
        Me.BTN_Replace = New System.Windows.Forms.Button
        Me.LBL_PMP_Status = New System.Windows.Forms.Label
        Me.BTN_Remove = New System.Windows.Forms.Button
        Me.BTN_Start = New System.Windows.Forms.Button
        Me.BTN_Stop = New System.Windows.Forms.Button
        Me.LBL_PricePerLitre = New System.Windows.Forms.Label
        Me.LBL_PetrolPumped = New System.Windows.Forms.Label
        Me.LBL_CurrentCost = New System.Windows.Forms.Label
        Me.LBL_PumpTime = New System.Windows.Forms.Label
        Me.LBL_PPL_VAL = New System.Windows.Forms.Label
        Me.LBL_PP_VAL = New System.Windows.Forms.Label
        Me.LBL_CC_VAL = New System.Windows.Forms.Label
        Me.LBL_TPHO_VAL = New System.Windows.Forms.Label
        Me.TMR_Petrol = New System.Windows.Forms.Timer(Me.components)
        Me.SuspendLayout()
        '
        'BTN_Replace
        '
        Me.BTN_Replace.BackColor = System.Drawing.SystemColors.ControlDarkDark
        Me.BTN_Replace.Font = New System.Drawing.Font("Microsoft Sans Serif", 9.75!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.BTN_Replace.ForeColor = System.Drawing.SystemColors.ControlLightLight
        Me.BTN_Replace.Location = New System.Drawing.Point(366, 134)
        Me.BTN_Replace.Name = "BTN_Replace"
        Me.BTN_Replace.Size = New System.Drawing.Size(117, 33)
        Me.BTN_Replace.TabIndex = 3
        Me.BTN_Replace.Text = "Drop Handle"
        Me.BTN_Replace.UseVisualStyleBackColor = False
        '
        'LBL_PMP_Status
        '
        Me.LBL_PMP_Status.AutoSize = True
        Me.LBL_PMP_Status.BackColor = System.Drawing.SystemColors.ActiveCaptionText
        Me.LBL_PMP_Status.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        Me.LBL_PMP_Status.Font = New System.Drawing.Font("Microsoft Sans Serif", 9.75!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LBL_PMP_Status.Location = New System.Drawing.Point(520, 74)
        Me.LBL_PMP_Status.MinimumSize = New System.Drawing.Size(117, 33)
        Me.LBL_PMP_Status.Name = "LBL_PMP_Status"
        Me.LBL_PMP_Status.Size = New System.Drawing.Size(117, 33)
        Me.LBL_PMP_Status.TabIndex = 4
        Me.LBL_PMP_Status.Text = "Pump Status"
        Me.LBL_PMP_Status.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        '
        'BTN_Remove
        '
        Me.BTN_Remove.BackColor = System.Drawing.SystemColors.ControlText
        Me.BTN_Remove.Font = New System.Drawing.Font("Microsoft Sans Serif", 9.75!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.BTN_Remove.ForeColor = System.Drawing.SystemColors.ControlLightLight
        Me.BTN_Remove.Location = New System.Drawing.Point(366, 17)
        Me.BTN_Remove.Name = "BTN_Remove"
        Me.BTN_Remove.Size = New System.Drawing.Size(117, 33)
        Me.BTN_Remove.TabIndex = 5
        Me.BTN_Remove.Text = "Take Handle"
        Me.BTN_Remove.UseVisualStyleBackColor = False
        '
        'BTN_Start
        '
        Me.BTN_Start.BackColor = System.Drawing.SystemColors.ControlDarkDark
        Me.BTN_Start.Font = New System.Drawing.Font("Microsoft Sans Serif", 9.75!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.BTN_Start.ForeColor = System.Drawing.SystemColors.ControlLightLight
        Me.BTN_Start.Location = New System.Drawing.Point(397, 56)
        Me.BTN_Start.Name = "BTN_Start"
        Me.BTN_Start.Size = New System.Drawing.Size(117, 33)
        Me.BTN_Start.TabIndex = 6
        Me.BTN_Start.Text = "Squeeze"
        Me.BTN_Start.UseVisualStyleBackColor = False
        '
        'BTN_Stop
        '
        Me.BTN_Stop.BackColor = System.Drawing.SystemColors.ControlDarkDark
        Me.BTN_Stop.Font = New System.Drawing.Font("Microsoft Sans Serif", 9.75!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.BTN_Stop.ForeColor = System.Drawing.SystemColors.ControlLightLight
        Me.BTN_Stop.Location = New System.Drawing.Point(397, 95)
        Me.BTN_Stop.Name = "BTN_Stop"
        Me.BTN_Stop.Size = New System.Drawing.Size(117, 33)
        Me.BTN_Stop.TabIndex = 7
        Me.BTN_Stop.Text = "Unsqueeze"
        Me.BTN_Stop.UseVisualStyleBackColor = False
        '
        'LBL_PricePerLitre
        '
        Me.LBL_PricePerLitre.AutoSize = True
        Me.LBL_PricePerLitre.BackColor = System.Drawing.SystemColors.ActiveCaptionText
        Me.LBL_PricePerLitre.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        Me.LBL_PricePerLitre.Font = New System.Drawing.Font("Microsoft Sans Serif", 12.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LBL_PricePerLitre.Location = New System.Drawing.Point(12, 9)
        Me.LBL_PricePerLitre.MinimumSize = New System.Drawing.Size(200, 33)
        Me.LBL_PricePerLitre.Name = "LBL_PricePerLitre"
        Me.LBL_PricePerLitre.Size = New System.Drawing.Size(200, 33)
        Me.LBL_PricePerLitre.TabIndex = 8
        Me.LBL_PricePerLitre.Text = "Price Per Litre: "
        Me.LBL_PricePerLitre.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        '
        'LBL_PetrolPumped
        '
        Me.LBL_PetrolPumped.AutoSize = True
        Me.LBL_PetrolPumped.BackColor = System.Drawing.SystemColors.ActiveCaptionText
        Me.LBL_PetrolPumped.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        Me.LBL_PetrolPumped.Font = New System.Drawing.Font("Microsoft Sans Serif", 12.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LBL_PetrolPumped.Location = New System.Drawing.Point(12, 52)
        Me.LBL_PetrolPumped.MinimumSize = New System.Drawing.Size(200, 33)
        Me.LBL_PetrolPumped.Name = "LBL_PetrolPumped"
        Me.LBL_PetrolPumped.Size = New System.Drawing.Size(200, 33)
        Me.LBL_PetrolPumped.TabIndex = 9
        Me.LBL_PetrolPumped.Text = "Petrol Pumped: "
        Me.LBL_PetrolPumped.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        '
        'LBL_CurrentCost
        '
        Me.LBL_CurrentCost.AutoSize = True
        Me.LBL_CurrentCost.BackColor = System.Drawing.SystemColors.ActiveCaptionText
        Me.LBL_CurrentCost.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        Me.LBL_CurrentCost.Font = New System.Drawing.Font("Microsoft Sans Serif", 12.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LBL_CurrentCost.Location = New System.Drawing.Point(12, 95)
        Me.LBL_CurrentCost.MinimumSize = New System.Drawing.Size(200, 33)
        Me.LBL_CurrentCost.Name = "LBL_CurrentCost"
        Me.LBL_CurrentCost.Size = New System.Drawing.Size(200, 33)
        Me.LBL_CurrentCost.TabIndex = 10
        Me.LBL_CurrentCost.Text = "Current Cost: "
        Me.LBL_CurrentCost.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        '
        'LBL_PumpTime
        '
        Me.LBL_PumpTime.AutoSize = True
        Me.LBL_PumpTime.BackColor = System.Drawing.SystemColors.ActiveCaptionText
        Me.LBL_PumpTime.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        Me.LBL_PumpTime.Font = New System.Drawing.Font("Microsoft Sans Serif", 12.0!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LBL_PumpTime.Location = New System.Drawing.Point(12, 139)
        Me.LBL_PumpTime.MinimumSize = New System.Drawing.Size(200, 33)
        Me.LBL_PumpTime.Name = "LBL_PumpTime"
        Me.LBL_PumpTime.Size = New System.Drawing.Size(200, 33)
        Me.LBL_PumpTime.TabIndex = 11
        Me.LBL_PumpTime.Text = "Time Pump Has Been On: "
        Me.LBL_PumpTime.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        '
        'LBL_PPL_VAL
        '
        Me.LBL_PPL_VAL.AutoSize = True
        Me.LBL_PPL_VAL.BackColor = System.Drawing.SystemColors.ControlLightLight
        Me.LBL_PPL_VAL.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        Me.LBL_PPL_VAL.Font = New System.Drawing.Font("Microsoft Sans Serif", 12.0!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LBL_PPL_VAL.Location = New System.Drawing.Point(218, 9)
        Me.LBL_PPL_VAL.MinimumSize = New System.Drawing.Size(140, 33)
        Me.LBL_PPL_VAL.Name = "LBL_PPL_VAL"
        Me.LBL_PPL_VAL.Size = New System.Drawing.Size(140, 33)
        Me.LBL_PPL_VAL.TabIndex = 12
        Me.LBL_PPL_VAL.Text = "000"
        Me.LBL_PPL_VAL.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        '
        'LBL_PP_VAL
        '
        Me.LBL_PP_VAL.AutoSize = True
        Me.LBL_PP_VAL.BackColor = System.Drawing.SystemColors.ControlLightLight
        Me.LBL_PP_VAL.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        Me.LBL_PP_VAL.Font = New System.Drawing.Font("Microsoft Sans Serif", 12.0!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LBL_PP_VAL.Location = New System.Drawing.Point(218, 52)
        Me.LBL_PP_VAL.MinimumSize = New System.Drawing.Size(140, 33)
        Me.LBL_PP_VAL.Name = "LBL_PP_VAL"
        Me.LBL_PP_VAL.Size = New System.Drawing.Size(140, 33)
        Me.LBL_PP_VAL.TabIndex = 13
        Me.LBL_PP_VAL.Text = "000"
        Me.LBL_PP_VAL.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        '
        'LBL_CC_VAL
        '
        Me.LBL_CC_VAL.AutoSize = True
        Me.LBL_CC_VAL.BackColor = System.Drawing.SystemColors.ControlLightLight
        Me.LBL_CC_VAL.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        Me.LBL_CC_VAL.Font = New System.Drawing.Font("Microsoft Sans Serif", 12.0!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LBL_CC_VAL.Location = New System.Drawing.Point(218, 95)
        Me.LBL_CC_VAL.MinimumSize = New System.Drawing.Size(140, 33)
        Me.LBL_CC_VAL.Name = "LBL_CC_VAL"
        Me.LBL_CC_VAL.Size = New System.Drawing.Size(140, 33)
        Me.LBL_CC_VAL.TabIndex = 14
        Me.LBL_CC_VAL.Text = "000"
        Me.LBL_CC_VAL.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        '
        'LBL_TPHO_VAL
        '
        Me.LBL_TPHO_VAL.AutoSize = True
        Me.LBL_TPHO_VAL.BackColor = System.Drawing.SystemColors.ControlLightLight
        Me.LBL_TPHO_VAL.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        Me.LBL_TPHO_VAL.Font = New System.Drawing.Font("Microsoft Sans Serif", 12.0!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LBL_TPHO_VAL.Location = New System.Drawing.Point(218, 139)
        Me.LBL_TPHO_VAL.MinimumSize = New System.Drawing.Size(140, 33)
        Me.LBL_TPHO_VAL.Name = "LBL_TPHO_VAL"
        Me.LBL_TPHO_VAL.Size = New System.Drawing.Size(140, 33)
        Me.LBL_TPHO_VAL.TabIndex = 15
        Me.LBL_TPHO_VAL.Text = "000"
        Me.LBL_TPHO_VAL.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        '
        'TMR_Petrol
        '
        Me.TMR_Petrol.Enabled = True
        Me.TMR_Petrol.Interval = 1000
        '
        'FRM_Pump
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.BackColor = System.Drawing.SystemColors.Desktop
        Me.ClientSize = New System.Drawing.Size(644, 184)
        Me.Controls.Add(Me.LBL_TPHO_VAL)
        Me.Controls.Add(Me.LBL_CC_VAL)
        Me.Controls.Add(Me.LBL_PP_VAL)
        Me.Controls.Add(Me.LBL_PPL_VAL)
        Me.Controls.Add(Me.LBL_PumpTime)
        Me.Controls.Add(Me.LBL_CurrentCost)
        Me.Controls.Add(Me.LBL_PetrolPumped)
        Me.Controls.Add(Me.LBL_PricePerLitre)
        Me.Controls.Add(Me.BTN_Stop)
        Me.Controls.Add(Me.BTN_Start)
        Me.Controls.Add(Me.BTN_Remove)
        Me.Controls.Add(Me.LBL_PMP_Status)
        Me.Controls.Add(Me.BTN_Replace)
        Me.Name = "FRM_Pump"
        Me.Text = "Petrol Pump Simulator"
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub
    Friend WithEvents BTN_Replace As System.Windows.Forms.Button
    Friend WithEvents LBL_PMP_Status As System.Windows.Forms.Label
    Friend WithEvents BTN_Remove As System.Windows.Forms.Button
    Friend WithEvents BTN_Start As System.Windows.Forms.Button
    Friend WithEvents BTN_Stop As System.Windows.Forms.Button
    Friend WithEvents LBL_PricePerLitre As System.Windows.Forms.Label
    Friend WithEvents LBL_PetrolPumped As System.Windows.Forms.Label
    Friend WithEvents LBL_CurrentCost As System.Windows.Forms.Label
    Friend WithEvents LBL_PumpTime As System.Windows.Forms.Label
    Friend WithEvents LBL_PPL_VAL As System.Windows.Forms.Label
    Friend WithEvents LBL_PP_VAL As System.Windows.Forms.Label
    Friend WithEvents LBL_CC_VAL As System.Windows.Forms.Label
    Friend WithEvents LBL_TPHO_VAL As System.Windows.Forms.Label
    Friend WithEvents TMR_Petrol As System.Windows.Forms.Timer

End Class
